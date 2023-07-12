# This script runs a benchmark for EXTERNAL measurement of TIME
# 
# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)

QUERY=$1
# DATA_SET=$(echo $QUERY | cut -d "/" -f 1)
NUM_JOINS=$2
DEVICE=${3:-"gpu"}
N_REPEAT=15
FILE="results/external_log/$DEVICE/overhead.csv"

echo "Benchmarking $1 ..."
if [ ! -f /tmp/foo.txt ]; then
    HEAD="query"
    for i in $(seq $N_REPEAT)
    do
        HEAD=$HEAD";time_"$i
    done
    echo $HEAD >> $FILE
fi

echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> $FILE

for i in $(seq $N_REPEAT)
do
    echo "run "$i" of "$N_REPEAT
    start=$(date +%s.%N)
    python3 main.py run $QUERY 0 --$DEVICE --skip-joins
    runtime=$(echo "$(date +%s.%N) - $start" | bc)
    log=$log";"$runtime
done
echo $log
echo $log >> $FILE
