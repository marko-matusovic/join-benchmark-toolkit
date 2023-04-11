
echo "Benchmarking $1 ..."
while read p; do
    for i in {1..5}   # you can also use {0..9}
    do
        # time python3.11 main.py time_mem $1 $p
        python3 main.py time_mem $1 $p
    done
done <scripts/perms/$2.csv
