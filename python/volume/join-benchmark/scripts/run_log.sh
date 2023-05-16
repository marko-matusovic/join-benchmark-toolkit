echo "Benchmarking $1 ..."
echo "join_order;time_total;mem_peak" >> "results/external_log/"$1".csv"
echo "// Timestamp "`date +"%Y-%m-%dT%H:%M:%S"` >> "results/external_log/"$1".csv"
while read p; do
    for i in {1..5}   # you can also use {0..9}
    do
        start=`date +%s`
        python3 main.py run $1 $p
        end=`date +%s`

        runtime=$((end-start))
        
        echo $p";"$runtime";" >> "results/external_log/"$1".csv"
    done
done <scripts/perms/$2.csv
