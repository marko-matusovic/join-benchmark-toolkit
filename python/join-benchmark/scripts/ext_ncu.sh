# This script runs a benchmark and performs GPU PROFILING
# 
# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)

echo "Benchmarking $1 ..."

QUERY=$1

while read PERM; do
    
    LOG_FILE="results/ncu/"$QUERY"/"$PERM".csv"
    echo "saving to '"$LOG_FILE"'"
    
    ncu -f --csv \
        --metrics "regex:^dram__bytes_(read|write).sum$" \
        --log-file $LOG_FILE \
        python3 main.py run $QUERY $PERM --GPU

done <scripts/perms/$2.csv
