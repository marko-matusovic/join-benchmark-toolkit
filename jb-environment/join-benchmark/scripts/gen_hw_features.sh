#!/bin/bash

HW_NAME=$1
if [ -z "$HW_NAME" ]; then
    echo "Error: HW name is empty! You should call this script with 1 positional argument, which is the name of the hardware this is running on."
    exit 1
fi

OTHER_ARGS=${@:2}

# DEVICE="cpu" # do both?
DEVICE="gpu"
for arg in "$@"
do
    if [ "$arg" == "--cpu" ]; then
        DEVICE="cpu"
    fi
done


N_REPEAT=10
CUR_DIR=$(dirname $(realpath $0))
RES_FILE="$CUR_DIR/../results/training_data/$DB_SET/features_hw_${HW_NAME}.csv"

echo "TIMESTAMP;DB_SET/QUERY;DEVICE;EXIT_CODE;PARSING;OVERHEAD;FILTERS;JOINS" >> $RES_FILE
echo "# CREATED AT $(date +"[%Y-%m-%dT%H:%M:%S]")" >> $RES_FILE

for i in $CUR_DIR/../data/hwp/queries/*
do
    QUERY=$(basename $i)
    QUERY="${QUERY%.*}"

    # Run x N_REPEAT
    for j in $(seq $N_REPEAT); do 
        TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
        LOG_START="$TIMESTAMP;$QUERY;$DEVICE"
        python3 main.py run hwp/$QUERY --$DEVICE --log-time $RES_FILE $LOG_START $OTHER_ARGS
        RES=$?
        if [[ $RES -ne 0 ]]; then
            echo "$LOG_START;$RES;;;;#FAILED" >> $RES_FILE
        fi;
    done
done

# RUN WITH 
# scripts/gen_hw_features.sh {hw_name}
