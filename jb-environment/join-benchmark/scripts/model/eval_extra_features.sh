#! /bin/bash

EVAL=${1:-"job,tpcds"}
FIT=${2:-"ssb"}

CURRENT_DIR=$(dirname "$0")
RES_DIR=$(cd "$CURRENT_DIR/../../results" && pwd)

CORE_FEATURE="t_length"
# ⬇️ base
# EXTRA_FEATURES=("" "t_unique" "t_id_size" "t_row_size" "t_cache_age" "t_cluster_size" "t_bounds_low" "t_bounds_high" "t_bounds_range" "c_len_res" "c_len_possible_max" "c_len_unique_max" "c_selectivity" "c_cluster_size" "c_cluster_overlap" "c_tbl_ratio_length" "c_tbl_ratio_unique" "c_tbl_ratio_row_size" "c_tbl_ratio_cache_age" "c_tbl_ratio_bounds_range")
# ⬇️ includes c_ratio values
EXTRA_FEATURES=("" "t_unique" "t_id_size" "t_row_size" "t_cache_age" "t_cluster_size" "t_bounds_low" "t_bounds_high" "t_bounds_range" "c_len_res" "c_len_possible_max" "c_len_unique_max" "c_selectivity" "c_cluster_size" "c_cluster_overlap" "c_tbl_ratio_length" "c_tbl_ratio_unique" "c_tbl_ratio_row_size" "c_tbl_ratio_cache_age" "c_tbl_ratio_bounds_range")
# ⬇️ includes c_min and c_max values
# EXTRA_FEATURES=("" "t_unique" "t_id_size" "t_row_size" "t_cache_age" "t_cluster_size" "t_bounds_low" "t_bounds_high" "t_bounds_range" "c_len_res" "c_len_possible_max" "c_len_unique_max" "c_selectivity" "c_cluster_size" "c_cluster_overlap" "c_tbl_ratio_length" "c_tbl_ratio_unique" "c_tbl_ratio_row_size" "c_tbl_ratio_cache_age" "c_tbl_ratio_bounds_range" "c_tbl_min_length" "c_tbl_min_unique" "c_tbl_min_row_size" "c_tbl_min_cache_age" "c_tbl_min_bounds_range" "c_tbl_max_length" "c_tbl_max_unique" "c_tbl_max_row_size" "c_tbl_max_cache_age" "c_tbl_max_bounds_range")

for FEATURE in "${EXTRA_FEATURES[@]}"
do
    if [ -n "$FEATURE" ]; then
        SELECT="$CORE_FEATURE,$FEATURE"
    else
        SELECT="$CORE_FEATURE"
    fi

    echo "$SELECT set 4"
    python3 main.py train-eval-features $EVAL 4 --fit $FIT --features $SELECT --res-path $RES_DIR --log
    echo "$SELECT set 5"
    python3 main.py train-eval-features $EVAL 5 --fit $FIT --features $SELECT --res-path $RES_DIR --log
done

echo "Done"
