# This script runs a benchmark for EXTERNAL measurement of TIME
# 
# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)

QUERY=$1
NUM_JOINS=$2
DEVICE=${3:-"gpu"}
OTHER_ARGS=${@:4}
N_REPEAT=15

echo "Benchmarking $1 ..."

HEAD="join_order"
for i in $(seq $N_REPEAT)
do
    HEAD=$HEAD";time_"$1
done
echo $HEAD >> "results/external_log/$DEVICE/$1.csv"

echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> "results/external_log/$DEVICE/$1.csv"
echo "// Args $OTHER_ARGS" >> "results/external_log/$DEVICE/$1.csv"

while read PERM; do
    log=$PERM
    for i in $(seq $N_REPEAT)
    do
        start=$(date +%s.%N)
        python3 main.py run $QUERY $PERM --$DEVICE $OTHER_ARGS
        runtime=$(echo "$(date +%s.%N) - $start" | bc)
            
        echo "run "$i" of "$N_REPEAT" took "$runtime"s"
        log=$log";"$runtime
    done
    echo $log
    echo $log >> "results/external_log/$DEVICE/$1.csv"

done <scripts/perms/$NUM_JOINS.csv
