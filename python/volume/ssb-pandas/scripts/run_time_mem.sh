
echo "Benchmarking $1 ..."
echo "join_order;execution_tree;time_total;mem_peak;time_load;mem_load;time_filters;mem_filters;time_joins;mem_joins" >> "results/time_mem/"$1".csv"
echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> "results/time_mem/"$1".csv"
while read p; do
    for i in {1..5}   # you can also use {0..9}
    do
        # time python3 main.py time_mem $1 $p
        python3 main.py time_mem $1 $p
    done
done <scripts/perms/$2.csv
