# This script runs a time and memory cost-model calculations for permutations
# 
# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)

echo "Benchmarking $1 ..."
echo "operation_name;T1_name;T2_name;T1_real_len;T1_approx_len;T2_real_len;T2_approx_len;R_real_len;R_approx_len;real_selectivity;approx_selectivity" >> "results/comp_card_est/$1.csv"
echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> "results/comp_card_est/$1.csv"

QUERY=$1
NUM_JOINS=$2
while read PERM; do
    echo "// Perm: [$PERM]" >> "results/comp_card_est/$1.csv"
    python3 main.py comp_card_est $QUERY $PERM
done <scripts/perms/$NUM_JOINS.csv
