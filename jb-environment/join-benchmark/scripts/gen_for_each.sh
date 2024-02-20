#!/bin/bash

# Run from project root, not from scripts folder. So from scripts/../ which is join-benchmark folder

SCENARIO=$1
DB_SET=$2
GEN_RUN=${3:-$((1000 + $RANDOM % 9000))}
OTHER_ARGS=$4

# Load in values and executable from scenario
source $SCENARIO

RES_FILE="./results/training_data/$DB_SET/set_${GEN_RUN}_${SCENARIO_NAME}.csv"

TIMESTAMP=$(date +"[%Y-%m-%dT%H:%M:%S]")
if [ -f $RES_FILE ]; then
    echo "Attaching to a training set_$GEN_RUN"
    echo "# RESUMING RUN AT $TIMESTAMP" >>$RES_FILE
else
    echo "Starting a new training set_$GEN_RUN"
    mkdir ./results/perms_pos/$DB_SET/$GEN_RUN
    echo $CSV_HEADER >>$RES_FILE
    echo "# CREATED AT $TIMESTAMP" >>$RES_FILE
fi

case $DB_SET in
'ssb')
    QUERIES=("q11" "q12" "q13" "q21" "q22" "q23" "q31" "q32" "q33" "q34" "q41" "q42" "q43")
    NUMS_JOIN=("1" "1" "1" "3" "3" "3" "3" "3" "3" "3" "4" "4" "4")
    ;;
'job')
    # QUERIES=("1a" "1b" "1c" "1d" "2a" "2b" "2c" "2d" "3a" "3b" "3c" "4a" "4b" "4c" "5a" "5b" "5c" "6a" "6b" "6c" "6d" "6e" "6f" "7b" "8a" "8b" "8c" "8d" "9a" "9b" "9c" "9d" "10a" "10b" "10c" "11a" "11b" "11c" "11d" "12a" "12b" "12c" "13a" "13b" "13c" "13d" "14a" "14b" "14c" "15a" "15b" "15c" "15d" "16a" "16b" "16c" "16d" "17a" "17b" "17c" "17d" "17e" "17f" "18a" "18b" "18c" "19a" "19b" "19c" "19d" "20a" "20b" "20c" "21a" "21b" "21c" "22a" "22b" "22c" "22d" "23a" "23b" "23c" "24a" "24b" "25a" "25b" "25c" "26a" "26b" "26c" "27a" "27b" "27c" "28a" "28b" "28c" "29a" "29b" "29c" "30a" "30b" "30c" "31a" "31b" "31c" "32a" "32b" "33a" "33b" "33c")
    # NUMS_JOIN=("5" "5" "5" "5" "5" "5" "5" "5" "4" "4" "4" "5" "5" "5" "5" "5" "5" "5" "5" "5" "5" "5" "5" "11" "7" "8" "7" "7" "9" "9" "9" "9" "7" "7" "7" "10" "10" "10" "10" "8" "8" "8" "11" "11" "11" "11" "10" "10" "10" "14" "14" "14" "14" "11" "11" "11" "11" "9" "9" "9" "9" "9" "9" "9" "9" "9" "13" "13" "13" "13" "12" "12" "12" "14" "14" "14" "16" "16" "16" "16" "16" "16" "16" "18" "18" "14" "14" "14" "17" "17" "17" "21" "21" "21" "23" "23" "23" "28" "28" "28" "21" "21" "21" "20" "20" "20" "3" "3" "3" "3" "3" )
    ### ⬆️ all queries, ⬇️ working queries
    # QUERIES=("1a" "1b" "1c" "1d" "2a" "2b" "2c" "2d" "3a" "3b" "3c" "4a" "4b" "4c" "5a" "5b" "5c" "6a" "6b" "6c" "6d" "6e" "6f" "7b" "8a" "8b" "9b" "9c" "9d" "10a" "10b" "10c" "12a" "12c" "13a" "13b" "13c" "13d" "14a" "14b" "15b" "18a" "18c" "22a" "22b" "25a" "25b" "25c" "28b" "29a" "29b" "29c" "30a" "30b" "30c" "31b" "32a" "32b" "33a" "33b" "33c")
    # NUMS_JOIN=("5" "5" "5" "5" "5" "5" "5" "5" "4" "4" "4" "5" "5" "5" "5" "5" "5" "5" "5" "5" "5" "5" "5" "11" "7" "8" "9" "9" "9" "7" "7" "7" "8" "8" "11" "11" "11" "11" "10" "10" "14" "9" "9" "16" "16" "14" "14" "14" "23" "28" "28" "28" "21" "21" "21" "20" "3" "3" "3" "3" "3")
    ### ⬇️ selected
    # QUERIES=("2a" "6f" "8c" "9d" "11d" "12a" "13a" "14a" "17e" "18b")
    # NUMS_JOIN=("5" "5" "8" "9" "10" "8" "11" "10" "9" "9")
    ### ⬇️ selected x2
    QUERIES=("2a" "8c" "9d" "13a" "14a")
    NUMS_JOIN=("5" "8" "9" "11" "10")
    ;;
'tpcds')
    # QUERIES=("query_3" "query_12" "query_17" "query_20" "query_22" "query_25" "query_27" "query_36" "query_42" "query_43" "query_50" "query_52" "query_55" "query_96")
    # NUMS_JOIN=("2" "2" "10" "2" "2" "10" "4" "3" "2" "2" "6" "2" "2" "3")
    ### ⬆️ all queries, ⬇️ selected
    QUERIES=("query_17" "query_25" "query_27" "query_29" "query_50")
    NUMS_JOIN=("10" "10" "4" "10" "6")
    ;;
*)
    echo "Unsupported Dataset passed, choose from [\"ssb\", \"job\", \"tpcds\"]"
    exit 1
    ;;
esac

# REPEAT UNTIL STOPPED EXTERNALLY
while :; do
    TOUCHED=false
    for i in "${!QUERIES[@]}"; do

        QUERY=${QUERIES[i]}
        NUM_JOINS=${NUMS_JOIN[i]}

        PERM_FILE="./scripts/perms/$NUM_JOINS.csv"
        NUM_PERMS=$(wc -l <$PERM_FILE)
        NUM_PERMS=$((NUM_PERMS))

        POS_FILE="./results/perms_pos/$DB_SET/$GEN_RUN/${QUERY}_${SCENARIO_NAME}"
        if [ ! -f $POS_FILE ]; then
            echo "Creating new file \"$POS_FILE\""
            echo 0 >$POS_FILE
        fi
        POS=$(cat $POS_FILE)

        POS=$((POS + 1))
        if (($NUM_PERMS < $POS)); then continue; fi
        PERM=$(sed "${POS}q;d" $PERM_FILE)

        echo $PERM

        # Run x N_REPEAT
        for j in $(seq $N_REPEAT); do execute; done

        # store the new POS only when finished, when aborted mid repeat, redo the perm
        echo $POS >$POS_FILE
        TOUCHED=true
    done

    if [[ ! $TOUCHED ]]; then break; fi

done

# RUN WITH
# scripts/gen_data.sh scripts/gen_data/{scenario} {db_set} {training_set}

# RESET WITH
# rm -rf results/perms_pos/{db_set}/{training_set}/* & rm results/training_data/{db_set}/set_{training_set}_{scenario_name}.csv
