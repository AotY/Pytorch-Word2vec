#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2019 LeonTao
#
# Distributed under terms of the MIT license.

"""
Covert questions data to learning embedding format.
"""

import argparse
from tqdm import tqdm



parser = argparse.ArgumentParser()
parser.add_argument('--question_', type=str, default='./data/', help="data directory path")
parser.add_argument('--corpus_path', type=str, default='./data/corpus.txt', help="corpus path for building vocab")
args = parser.parse_args()

corpus_file = open(args.corpus_path, 'w', encoding='utf-8')
with open(args.questions_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip()
        sub = line.split('SPLIT')

        query = sub[2]
        response = sub[3]

        corpus_file.write('%s\n' % query)
        corpus_file.write('%s\n' % response)

corpus_file.close()

