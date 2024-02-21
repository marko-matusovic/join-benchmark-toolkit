#!/bin/bash

SCENARIO_NAME="measurements"
CSV_HEADER="TIMESTAMP;DB_SET/QUERY;DEVICE;TYPE_OF_RUN;JOIN_PERMUTATION;EXIT_CODE;PARSING;OVERHEAD;FILTERS;JOINS"
N_REPEAT=10
DEVICE="cpu"

function execute(){
    TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
    LOG_START="$TIMESTAMP;$DB_SET/$QUERY;$DEVICE;0;$PERM"
    python3 main.py run $DB_SET/$QUERY --jo $PERM --$DEVICE --log-time $RES_FILE $LOG_START $OTHER_ARGS
    RES=$?
    if [[ $RES -ne 0 ]]; then
        echo "$LOG_START;$RES;;;;#FAILED" >> $RES_FILE
    fi;
    return $RES
}
