#!/usr/bin/env bash
#
# build_corpus.sh
# Copyright (C) 2019 LeonTao
#
# Distributed under terms of the MIT license.
#

mkdir -p data/

python ./build_corpus.py \
    --questions_path /home/deep/Public/Research/cleaned.questions.txt \
    --corpus_path ./data/corpus.txt \
    
/
