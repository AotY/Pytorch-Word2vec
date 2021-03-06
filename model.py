# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import numpy as np

class Bundler(nn.Module):

    def forward(self, data):
        raise NotImplementedError

    def forward_i(self, data):
        raise NotImplementedError

    def forward_o(self, data):
        raise NotImplementedError


class Word2Vec(Bundler):

    def __init__(self, vocab_size=20000, embedding_size=300, padding_idx=0):
        super(Word2Vec, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size

        self.ivectors = nn.Embedding(self.vocab_size, self.embedding_size, padding_idx=padding_idx)
        self.ovectors = nn.Embedding(self.vocab_size, self.embedding_size, padding_idx=padding_idx)

        # init
        self.ivectors.weight = nn.Parameter(torch.cat([torch.zeros(1, self.embedding_size), torch.FloatTensor(self.vocab_size - 1, self.embedding_size).uniform_(-0.5 / self.embedding_size, 0.5 / self.embedding_size)]))
        self.ovectors.weight = nn.Parameter(torch.cat([torch.zeros(1, self.embedding_size), torch.FloatTensor(self.vocab_size - 1, self.embedding_size).uniform_(-0.5 / self.embedding_size, 0.5 / self.embedding_size)]))

        self.ivectors.weight.requires_grad = True
        self.ovectors.weight.requires_grad = True

    def forward(self, data):
        return self.forward_i(data)

    def forward_i(self, data):
        v = torch.LongTensor(data)
        v = v.cuda() if self.ivectors.weight.is_cuda else v
        return self.ivectors(v)

    def forward_o(self, data):
        v = torch.LongTensor(data)
        v = v.cuda() if self.ovectors.weight.is_cuda else v
        return self.ovectors(v)


class SGNS(nn.Module):

    def __init__(self, wrod2vec, vocab_size=20000, n_negs=20, weights=None):
        super(SGNS, self).__init__()
        self.wrod2vec = wrod2vec
        self.vocab_size = vocab_size

        self.n_negs = n_negs
        self.weights = None

        if weights is not None:
            wf = np.power(weights, 0.75)
            wf = wf / wf.sum()
            self.weights = torch.FloatTensor(wf)

    def forward(self, iword, owords):
        batch_size = iword.size()[0]
        context_size = owords.size()[1]

        # negative sample
        if self.weights is not None:
            nwords = torch.multinomial(self.weights, batch_size * context_size * self.n_negs, replacement=True).view(batch_size, -1)
        else:
            nwords = torch.FloatTensor(batch_size, context_size * self.n_negs).uniform_(0, self.vocab_size - 1).long()

        ivectors = self.wrod2vec.forward_i(iword).unsqueeze(2)

        ovectors = self.wrod2vec.forward_o(owords)

        nvectors = self.wrod2vec.forward_o(nwords).neg()

        oloss = torch.bmm(ovectors, ivectors).squeeze().sigmoid().log().mean(1)

        nloss = torch.bmm(nvectors, ivectors).squeeze().sigmoid().log().view(-1, context_size, self.n_negs).sum(2).mean(1)

        # loss
        return -(oloss + nloss).mean()
