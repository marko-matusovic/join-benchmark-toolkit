# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)
# 3rd arg: additional args to pass on to python (usually --gpu to run on GPU)

echo "Benchmarking $1 ..."
echo "join_order;time_total;mem_peak" >> "results/external_log/cpu/"$1".csv"
echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> "results/external_log/cpu/"$1".csv"
while read p; do
    for i in {1..5}   # you can also use {0..9}
    do
        start=$(date +%s.%N)
        
        if python3 main.py run $1 $p $3; then 
            runtime=$(echo "$(date +%s.%N) - $start" | bc)
            
            log="["$p"];"$runtime";"
            echo $log
            echo $log >> "results/external_log/cpu/"$1".csv"
        else
            echo 'terminated with error, skipping'
        fi
    done
done <scripts/perms/$2.csv
