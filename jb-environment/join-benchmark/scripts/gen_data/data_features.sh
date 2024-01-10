#!/bin/bash

SCENARIO_NAME="features_data"
CSV_HEADER="TIMESTAMP;DB_SET/QUERY;JOIN_PERMUTATION;JOIN_ID;FEATURES"
N_REPEAT=1

function execute(){
    TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
    LOG_START="$TIMESTAMP;$DB_SET/$QUERY;$PERM"
    python3 main.py features $DB_SET/$QUERY --jo $PERM --log $RES_FILE $LOG_START $OTHER_ARGS
    RES=$?
    if [[ $RES -ne 0 ]]; then
        echo "$LOG_START;;#FAILED" >> $RES_FILE
    fi;
}
