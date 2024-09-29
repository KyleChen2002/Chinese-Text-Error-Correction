#!/bin/sh
TOKENIZERS_PARALLELISM=true
export TOKENIZERS_PARALLELISM

python3 train.py $@
