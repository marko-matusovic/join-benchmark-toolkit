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
N_REPEAT=10
OTHER_ARGS=$3

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
        QUERIES=("1a" "1b" "1c" "1d" "2a" "2b" "2c" "2d" "3a" "3b" "3c" "4a" "4b" "4c" "5a" "5b" "5c" "6a" "6b" "6c" "6d" "6e" "6f" "7b" "8a" "8b" "8c" "8d" "9a" "9b" "9c" "9d" "10a" "10b" "10c" "11a" "11b" "11c" "11d" "12a" "12b" "12c" "13a" "13b" "13c" "13d" "14a" "14b" "14c" "15a" "15b" "15c" "15d" "16a" "16b" "16c" "16d" "17a" "17b" "17c" "17d" "17e" "17f" "18a" "18b" "18c" "19a" "19b" "19c" "19d" "20a" "20b" "20c" "21a" "21b" "21c" "22a" "22b" "22c" "22d" "23a" "23b" "23c" "24a" "24b" "25a" "25b" "25c" "26a" "26b" "26c" "27a" "27b" "27c" "28a" "28b" "28c" "29a" "29b" "29c" "30a" "30b" "30c" "31a" "31b" "31c" "32a" "32b" "33a" "33b" "33c")
        NUMS_JOIN=("5" "5" "5" "5" "5" "5" "5" "5" "4" "4" "4" "5" "5" "5" "5" "5" "5" "5" "5" "5" "5" "5" "5" "11" "7" "8" "7" "7" "9" "9" "9" "9" "7" "7" "7" "10" "10" "10" "10" "8" "8" "8" "11" "11" "11" "11" "10" "10" "10" "14" "14" "14" "14" "11" "11" "11" "11" "9" "9" "9" "9" "9" "9" "9" "9" "9" "13" "13" "13" "13" "12" "12" "12" "14" "14" "14" "16" "16" "16" "16" "16" "16" "16" "18" "18" "14" "14" "14" "17" "17" "17" "21" "21" "21" "23" "23" "23" "28" "28" "28" "21" "21" "21" "20" "20" "20" "3" "3" "3" "3" "3" )
        ;;
    # 'tpcds')
    #     QUERIES=("q11" "q12" "q13" "q21" "q22" "q23" "q31" "q32" "q33" "q34" "q41" "q42" "q43")
    #     NUMS_JOIN=("1" "1" "1" "3" "3" "3" "3" "3" "3" "3" "4" "4" "4")
    #     ;;
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

        POS=$((POS+1))
        if (( $NUM_PERMS < $POS )); then continue; fi;
        PERM=$(sed "${POS}q;d" $PERM_FILE)

        echo $PERM

        # Run x N_REPEAT
        for j in $(seq $N_REPEAT); do
            # START=$(date +%s.%N)
            TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
            LOG_START="$TIMESTAMP;$DB_SET/$QUERY;$DEVICE;0;$PERM"
            python3 main.py run $DB_SET/$QUERY --jo $PERM --$DEVICE --log-time $RES_FILE $LOG_START $OTHER_ARGS
            RES=$?
            if [[ $RES -ne 0 ]]; then
                echo "$LOG_START;$RES;;;;" >> $RES_FILE
            fi;
            # RUNTIME=$(echo "$(date +%s.%N) - $START" | bc)
            # echo "$TIMESTAMP;$DB_SET/$QUERY;$DEVICE;0;$PERM;$RES;$RUNTIME"
            # echo "$TIMESTAMP;$DB_SET/$QUERY;$DEVICE;0;$PERM;$RES;$RUNTIME" >> $RES_FILE
        done

        # store the new POS only when finished, when aborted mid repeat, redo the perm
        echo $POS > $POS_FILE

    done
    
done

# # START WITH
# ./scripts/gen_data_runtime.sh ssb 2 "--db-path /data/db_data/ssb"

# # RESET
# rm -rf results/perms_pos/ssb/2
# rm results/training_data/ssb/set_2_measurement.csv 
