# This script runs a benchmark for EXTERNAL measurement of TIME
# 
# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)

echo "Benchmarking $1 ..."
echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> "results/external_log/gpu/"$1".csv"
echo "join_order;times..." >> "results/external_log/gpu/"$1".csv"

QUERY=$1
NUM_JOINS=$2
N_REPEAT=15

while read PERM; do
    log=$PERM
    for i in $(seq $N_REPEAT)
    do
        echo "run "$i" of "$N_REPEAT
        start=$(date +%s.%N)
        python3 main.py run $QUERY $PERM --GPU
        runtime=$(echo "$(date +%s.%N) - $start" | bc)
            
        log=$log";"$runtime
    done
    echo $log
    echo $log >> "results/external_log/gpu/"$1".csv"

done <scripts/perms/$NUM_JOINS.csv
