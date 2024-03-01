#! /bin/bash

NUM_OF_EXTRA=${1:-"1"}
EVAL=${2:-"ssb,job,tpcds"}
FIT=${3:-"ssb,job,tpcds"}
MORE_ARGS=${@:4}

if [[ $NUM_OF_EXTRA -ge 3 ]]; then
    echo "Too many extra features, only 0, 1, or 2 are allowed"
    exit 1
fi;

CURRENT_DIR=$(dirname "$0")
RES_DIR=$(cd "$CURRENT_DIR/../../results" && pwd)

CORE_FEATURE="t_length"
# ⬇️ base
# EXTRA_FEATURES=("t_unique" "t_id_size" "t_row_size" "t_cache_age" "t_cluster_size" "t_bounds_low" "t_bounds_high" "t_bounds_range" "c_len_res" "c_len_possible_max" "c_len_unique_max" "c_selectivity" "c_cluster_size" "c_cluster_overlap" "c_tbl_ratio_length" "c_tbl_ratio_unique" "c_tbl_ratio_row_size" "c_tbl_ratio_cache_age" "c_tbl_ratio_bounds_range")
# ⬇️ includes c_ratio values
# EXTRA_FEATURES=("t_unique" "t_id_size" "t_row_size" "t_cache_age" "t_cluster_size" "t_bounds_low" "t_bounds_high" "t_bounds_range" "c_len_res" "c_len_possible_max" "c_len_unique_max" "c_selectivity" "c_cluster_size" "c_cluster_overlap" "c_tbl_ratio_length" "c_tbl_ratio_unique" "c_tbl_ratio_row_size" "c_tbl_ratio_cache_age" "c_tbl_ratio_bounds_range")
# ⬇️ includes c_min and c_max values
EXTRA_FEATURES=("t_unique" "t_id_size" "t_row_size" "t_cache_age" "t_cluster_size" "t_bounds_low" "t_bounds_high" "t_bounds_range" "c_len_res" "c_len_possible_max" "c_len_unique_max" "c_selectivity" "c_cluster_size" "c_cluster_overlap" "c_tbl_ratio_length" "c_tbl_ratio_unique" "c_tbl_ratio_row_size" "c_tbl_ratio_cache_age" "c_tbl_ratio_bounds_range" "c_tbl_min_length" "c_tbl_min_unique" "c_tbl_min_row_size" "c_tbl_min_cache_age" "c_tbl_min_bounds_range" "c_tbl_max_length" "c_tbl_max_unique" "c_tbl_max_row_size" "c_tbl_max_cache_age" "c_tbl_max_bounds_range")


FEATURE_COMBS=($CORE_FEATURE)

if [[ $NUM_OF_EXTRA -gt 0 ]]; then
    for FEATURE1 in "${EXTRA_FEATURES[@]}"
    do
        SELECT1="$CORE_FEATURE,$FEATURE1"
        if [[ $NUM_OF_EXTRA == 1 ]]; then
            FEATURE_COMBS+=($SELECT1)
            continue
        fi
        for FEATURE2 in "${EXTRA_FEATURES[@]}"
        do
            if [[ $FEATURE1 == $FEATURE2 ]]; then continue; fi
            SELECT2="$SELECT1,$FEATURE2"
            if [[ $NUM_OF_EXTRA == 2 ]]; then
                FEATURE_COMBS+=($SELECT2)
                continue
            fi
            # # Too many, doesn't make sense to support it
            # for FEATURE3 in "${EXTRA_FEATURES[@]}"
            # do
            #     if [[ $FEATURE1 == $FEATURE3 || $FEATURE2 == $FEATURE3 ]]; then continue; fi
            #     SELECT3="$SELECT2,$FEATURE3"
            #     if [[ $NUM_OF_EXTRA == 3 ]]; then
            #         FEATURE_COMBS+=($SELECT3)
            #     fi
            # done
        done
    done
fi

# Iterate over the array and print each element on a new line
for item in ${FEATURE_COMBS[@]}; do
    echo "$item set 4"
    python3 main.py train-eval-features $EVAL 4 --fit $FIT --features $item --res-path $RES_DIR --log $MORE_ARGS
    echo "$item set 5"
    python3 main.py train-eval-features $EVAL 5 --fit $FIT --features $item --res-path $RES_DIR --log $MORE_ARGS
done


echo "Finished collecting results!"
