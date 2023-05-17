# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)
# 3rd arg: additional args to pass on to python (usually --gpu to run on GPU)

echo "Benchmarking $1 ..."
echo "join_order;execution_tree;time_total;mem_peak;time_load;mem_load;time_filters;mem_filters;time_joins;mem_joins" >> "results/time_mem/"$1".csv"
echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> "results/time_mem/"$1".csv"
while read p; do
    for i in {1..5}   # you can also use {0..9}
    do
        # time python3 main.py time_mem $1 $p
        python3 main.py time_mem $1 $p $3
    done
done <scripts/perms/$2.csv
