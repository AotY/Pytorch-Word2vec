#!/usr/bin/env bash
#
# train.sh
# Copyright (C) 2019 LeonTao
#
# Distributed under terms of the MIT license.
#


mkdir -p models/

export CUDA_VISIBLE_DEVICES=0

python ./train.sh \
    --name sgns \
    --data_dir data/ \
    --save_dir models/ \
    --e_dim 128 \
    --n_negs 7 \
    --epoch 100 \
    --batch_size 128 \
    --ss_t 1e-5 \
    --conti \
    --weights \
    --cuda \

/

