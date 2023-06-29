# This script runs a time and memory cost-model calculations for permutations
# 
# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)

echo "Benchmarking $1 ..."
echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> "results/compare_card_est/"$1".csv"
echo "table_name;real_length;approximated_length" >> "results/compare_card_est/"$1".csv"

QUERY=$1
NUM_JOINS=$2
while read PERM; do
    python3 main.py compare_card_est $QUERY $PERM
done <scripts/perms/$NUM_JOINS.csv
