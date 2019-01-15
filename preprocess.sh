#!/usr/bin/env bash
#
# preprocess.sh
# Copyright (C) 2019 LeonTao
#
# Distributed under terms of the MIT license.
#


mkdir -p data/

python ./preprocess.py \
    --data_dir data/ \
    --corpus_path data/corpus.txt \
    --window 5 \
    --max_vocab 50000 \

/

