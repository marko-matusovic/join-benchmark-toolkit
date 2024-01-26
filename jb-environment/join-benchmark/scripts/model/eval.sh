#!/bin/bash

CURRENT_DIR=$(dirname "$0")

# 1st {{ml_model: str}}             -> 
# 2st {{model1,model2: list[str]}}  -> model(s) to train on
# 3nd {{model3: str}}               -> model to evaluate
# 4rd {{set: int}}                  -> the set number
# --reg {{join_in_block: int}}      -> number of joins in a block
# --cls {{num_joins: int}}          -> number of join
# --train                           -> forces the model to train again

ML_MODEL=$1

# Parse the first argument as a string: models to train on
MODELS_TO_TRAIN_CM="$2"                        # separated with commas
MODELS_TO_TRAIN_US="${MODELS_TO_TRAIN_CM/,/_}" # separated with underscores

# Parse the second argument as the model to evaluate
MODEL_TO_EVAL="$3"

# Parse the third argument as the set number
SET_NUMBER="$4"

TRAIN=false
if [[ $@ == *--train* ]]; then
    TRAIN=true
fi

REG_OPTION=""
CLS_OPTION=""

while (("$#")); do
    case "$1" in
    --reg)
        REG_OPTION="$2"
        shift 2
        ;;
    --cls)
        CLS_OPTION="$2"
        shift 2
        ;;
    *)
        shift
        ;;
    esac
done

# Exit if invalid --cls and --reg options
if [[ (-z "$CLS_OPTION" && -z "$REG_OPTION") || (! -z "$CLS_OPTION" && ! -z "$REG_OPTION") ]]; then
    echo "Error, you must specify exactly one of --cls {num_joins: int} or --reg {join_in_block: int} arguments."
    exit 1
fi

if [[ (! -z "$CLS_OPTION") ]]; then
    ML="cls"
    MODEL_NAME="${ML_MODEL}_cls/set_${SET_NUMBER}_NJO${CLS_OPTION}_${MODELS_TO_TRAIN_US}"
    MODEL_PATH="${CURRENT_DIR}/../../results/models/${MODEL_NAME}.pickle"
    TRAIN_OPTION="--num-joins ${CLS_OPTION}"
fi
if [[ (! -z "$REG_OPTION") ]]; then
    ML="reg"
    MODEL_NAME="${ML_MODEL}_reg/set_${SET_NUMBER}_BS${REG_OPTION}_${MODELS_TO_TRAIN_US}"
    MODEL_PATH="${CURRENT_DIR}/../../results/models/${MODEL_NAME}.pickle"
    TRAIN_OPTION="--joins-in-block ${REG_OPTION}"
fi

# Parse the --train option
# also if there is no model file, we have to train!
if [[ $TRAIN == true ]] || [[ ! -f "$MODEL_PATH" ]]; then
    python3 main.py train-${ML_MODEL}-${ML} ${MODELS_TO_TRAIN_CM} ${SET_NUMBER} ${TRAIN_OPTION}
fi

python3 main.py eval-${ML_MODEL}-${ML} ${MODEL_TO_EVAL} ${SET_NUMBER} ${MODEL_NAME}
