#!/bin/bash

CURRENT_DIR=$(dirname "$0")

# 1st {{ML_TYPE: str}}              -> cls or reg
# 2st {{ML_MODEL: str}}             -> the name of the ML model to use
# 3st {{model1,model2: list[str]}}  -> model(s) to train on
# 4nd {{model3: str}}               -> model to evaluate
# 5rd {{set: int}}                  -> the set number
# 6th {{number: int}}               -> number (of joins in block (reg) or joins in query (cls))
# --train                           -> forces the model to train again

ML_TYPE=$1
ML_MODEL=$2

# Parse the first argument as a string: models to train on
MODELS_TO_TRAIN_CM="$3"                        # separated with commas
MODELS_TO_TRAIN_US="${MODELS_TO_TRAIN_CM/,/_}" # separated with underscores

MODEL_TO_EVAL="$4"
SET_NUMBER="$5"
NUM_OPTION="$6"

TRAIN=false
if [[ $@ == *--train* ]]; then
    TRAIN=true
fi

# ====================


if [[ "$ML_TYPE" == "cls" ]]; then
    MODEL_NAME="cls/${ML_MODEL}/set_${SET_NUMBER}_NJO${NUM_OPTION}_${MODELS_TO_TRAIN_US}"
    MODEL_PATH="${CURRENT_DIR}/../../results/models/${MODEL_NAME}.pickle"
    TRAIN_OPTION="--num-joins ${NUM_OPTION}"
fi
if [[ "$ML_TYPE" == "reg" ]]; then
    MODEL_NAME="reg/${ML_MODEL}/set_${SET_NUMBER}_BS${NUM_OPTION}_${MODELS_TO_TRAIN_US}"
    MODEL_PATH="${CURRENT_DIR}/../../results/models/${MODEL_NAME}.pickle"
    TRAIN_OPTION="--joins-in-block ${NUM_OPTION}"
fi

# Parse the --train option
# also if there is no model file, we have to train!
if [[ $TRAIN == true ]] || [[ ! -f "$MODEL_PATH" ]]; then
    python3 main.py train-${ML_TYPE} ${MODELS_TO_TRAIN_CM} ${SET_NUMBER} ${TRAIN_OPTION} --ml-model ${ML_MODEL}
fi

python3 main.py eval-${ML_TYPE} ${MODEL_TO_EVAL} ${SET_NUMBER} ${MODEL_NAME}
