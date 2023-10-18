#!/bin/bash

# Run from project root, not from scripts folder. So from scripts/../ which is join-benchmark folder
# 
# 1st arg: db_set to use to gen data [ssb, job]

DB_SET=$1
GEN_RUN=${2:-$((1000 + $RANDOM % 9000))}

# TODO: configure this in such way that once a run is started, the args cannot be canged, they are stored at start and read from a file when resumed
# DEVICE=${3:-"gpu"}
# N_REPEAT=${4:-"5"}
# OTHER_ARGS=${@:5}
DEVICE="gpu"
N_REPEAT=5
OTHER_ARGS=""

RES_FILE="./results/training_data/$DB_SET/set_${GEN_RUN}_measurement.csv"

TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
if [ -f $RES_FILE ]; then
    echo "Attaching to a training set_$GEN_RUN"
    echo "// RESUMING RUN AT $TIMESTAMP" >> $RES_FILE
else
    echo "Starting a new training set_$GEN_RUN"
    mkdir ./scripts/perms_pos/$DB_SET/$GEN_RUN
    echo "QUERY;TYPE_OF_RUN[0:OVERHEAD,1:JOIN_PERMUTATION];TIMESTAMP;MEASUREMENT" >> $RES_FILE
    echo "// CREATED AT $TIMESTAMP" >> $RES_FILE
fi;

if [ $DB_SET = 'ssb' ]; then
    
    OLDIFS=$IFS
    IFS=","
    # TODO: for loop can be parametrized to reduce duplicate code
    for i in q11,1 q12,1 q13,1 q21,3 q22,3 q23,3 q31,3 q32,3 q33,3 q34,3 q41,4 q42,4 q43,4; do
        set -- $i
        QUERY=$1
        NUM_JOINS=$2

        PERM_FILE="./scripts/perms/$NUM_JOINS.csv"
        NUM_PERMS=$(wc -l < $PERM_FILE)
        NUM_PERMS=$((NUM_PERMS))

        POS_FILE="./scripts/perms_pos/$DB_SET/$GEN_RUN/$QUERY"
        if [ ! -f $POS_FILE ]; then
            echo "Creating new file \"$POS_FILE\""
            echo 0 > $POS_FILE
        fi;
        POS=$(cat $POS_FILE)

        # Overhead x 1
        TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
        START=$(date +%s.%N)
        python3 main.py run $DB_SET/$QUERY 0 --$DEVICE --skip-joins
        RUNTIME=$(echo "$(date +%s.%N) - $START" | bc)
        echo "$QUERY;0;$TIMESTAMP;$RUNTIME"
        echo "$QUERY;0;$TIMESTAMP;$RUNTIME" >> $RES_FILE

        POS=$((POS+1))
        if (( $NUM_PERMS < $POS )); then POS=1; fi;
        PERM=$(sed "${POS}q;d" $PERM_FILE)

        # Run x N_REPEAT (5)
        for i in $(seq $N_REPEAT); do
            START=$(date +%s.%N)
            TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
            python3 main.py run $DB_SET/$QUERY $PERM --$DEVICE $OTHER_ARGS
            RUNTIME=$(echo "$(date +%s.%N) - $START" | bc)
            echo "$QUERY;1;$TIMESTAMP;$RUNTIME"
            echo "$QUERY;1;$TIMESTAMP;$RUNTIME" >> $RES_FILE
        done

        # store the new POS only when finished, when aborted mid repeat, redo the perm
        echo $POS > $POS_FILE

    done
    IFS=$OLDIFS

    
    

    
fi;
