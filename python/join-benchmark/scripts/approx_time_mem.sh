# This script runs a time and memory cost-model calculations for permutations
# 
# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)

echo "Benchmarking $1 ..."
echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> "results/approx_time_mem/"$1".csv"
echo "permutation;time_cost;memory_sum_cost;memory_max_cost" >> "results/approx_time_mem/"$1".csv"

QUERY=$1
NUM_JOINS=$2
while read PERM; do
    python3 main.py approx_time_mem $QUERY $PERM
done <scripts/perms/$NUM_JOINS.csv
