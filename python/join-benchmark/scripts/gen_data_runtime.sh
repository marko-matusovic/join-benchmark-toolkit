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
DEVICE="cpu"
N_REPEAT=1
OTHER_ARGS=""

RES_FILE="./results/training_data/$DB_SET/set_${GEN_RUN}_measurement.csv"

TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
if [ -f $RES_FILE ]; then
    echo "Attaching to a training set_$GEN_RUN"
    echo "// RESUMING RUN AT $TIMESTAMP" >> $RES_FILE
else
    echo "Starting a new training set_$GEN_RUN"
    mkdir ./results/perms_pos/$DB_SET/$GEN_RUN
    echo "TIMESTAMP;DB_SET/QUERY;DEVICE[cpu,gpu];TYPE_OF_RUN[1:OVERHEAD,0:JOIN_PERMUTATION];JOIN_PERMUTATION;EXIT_CODE[201:OK_SKIP_JOINS,200:OK,500:PROCESSING_ERROR];PARSING[MS];OVERHEAD[MS];FILTERS[LIST_MS];JOINS[LIST_MS]" >> $RES_FILE
    echo "// CREATED AT $TIMESTAMP" >> $RES_FILE
fi;

case $DB_SET in 
    'ssb')
        QUERIES=("q11" "q12" "q13" "q21" "q22" "q23" "q31" "q32" "q33" "q34" "q41" "q42" "q43")
        NUMS_JOIN=("1" "1" "1" "3" "3" "3" "3" "3" "3" "3" "4" "4" "4")
        ;;
    'job')
        QUERIES=("q11" "q12" "q13" "q21" "q22" "q23" "q31" "q32" "q33" "q34" "q41" "q42" "q43")
        NUMS_JOIN=("1" "1" "1" "3" "3" "3" "3" "3" "3" "3" "4" "4" "4")
        ;;
    'tpcds')
        QUERIES=("q11" "q12" "q13" "q21" "q22" "q23" "q31" "q32" "q33" "q34" "q41" "q42" "q43")
        NUMS_JOIN=("1" "1" "1" "3" "3" "3" "3" "3" "3" "3" "4" "4" "4")
        ;;
    *)
        echo "Unsupported Dataset passed, choose from [\"ssb\", \"job\"]"
        exit 1
esac

# REPEAT UNTIL STOPPED EXTERNALLY
while : ; do
    for i in "${!QUERIES[@]}"; do

        QUERY=${QUERIES[i]}
        NUM_JOINS=${NUMS_JOIN[i]}

        PERM_FILE="./scripts/perms/$NUM_JOINS.csv"
        NUM_PERMS=$(wc -l < $PERM_FILE)
        NUM_PERMS=$((NUM_PERMS))

        POS_FILE="./results/perms_pos/$DB_SET/$GEN_RUN/$QUERY"
        if [ ! -f $POS_FILE ]; then
            echo "Creating new file \"$POS_FILE\""
            echo 0 > $POS_FILE
        fi;
        POS=$(cat $POS_FILE)

        # Dropped overhead only, because we measure times individually
        # # Overhead x 1
        # # START=$(date +%s.%N)
        # TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
        # LOG_START="$TIMESTAMP;$DB_SET/$QUERY;$DEVICE;1;none"
        # python3 main.py run $DB_SET/$QUERY 0 --$DEVICE --skip-joins --log $RES_FILE $LOG_START $OTHER_ARGS
        # # RES=$?
        # # RUNTIME=$(echo "$(date +%s.%N) - $START" | bc)
        # # echo "$TIMESTAMP;$DB_SET/$QUERY;$DEVICE;1;none;$RES;$RUNTIME"
        # # echo "$TIMESTAMP;$DB_SET/$QUERY;$DEVICE;1;none;$RES;$RUNTIME" >> $RES_FILE

        POS=$((POS+1))
        if (( $NUM_PERMS < $POS )); then continue; fi;
        PERM=$(sed "${POS}q;d" $PERM_FILE)

        echo $PERM

        # Run x N_REPEAT (5)
        for j in $(seq $N_REPEAT); do
            # START=$(date +%s.%N)
            TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
            LOG_START="$TIMESTAMP;$DB_SET/$QUERY;$DEVICE;0;$PERM"
            python3 main.py run $DB_SET/$QUERY $PERM --$DEVICE --log $RES_FILE $LOG_START $OTHER_ARGS
            # RES=$?
            # RUNTIME=$(echo "$(date +%s.%N) - $START" | bc)
            # echo "$TIMESTAMP;$DB_SET/$QUERY;$DEVICE;0;$PERM;$RES;$RUNTIME"
            # echo "$TIMESTAMP;$DB_SET/$QUERY;$DEVICE;0;$PERM;$RES;$RUNTIME" >> $RES_FILE
        done

        # store the new POS only when finished, when aborted mid repeat, redo the perm
        echo $POS > $POS_FILE

    done
    
done
