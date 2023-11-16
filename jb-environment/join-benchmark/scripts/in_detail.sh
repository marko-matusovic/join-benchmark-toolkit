# This script runs a benchmark for INTERNAL measuring with DETAILED time stats
# 
# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)
# 3rd arg: additional args to pass on to python (usually --gpu to run on GPU)

RES_FILE="results/time_mem/"$1".csv"

echo "Benchmarking $1 ..."
echo "join_order;time_total;mem_peak;time_load;mem_load;time_filters;mem_filters;time_joins;mem_joins" >> $RES_FILE
echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> $RES_FILE
while read p; do
    for i in {1..5}   # you can also use {0..9}
    do
        # time python3 main.py time_mem $1 $p
        python3 main.py run $1 $p $3 --log-time-mem "$RES_FILE" "$p"
    done
done <scripts/perms/$2.csv
