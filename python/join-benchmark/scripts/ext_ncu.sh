# This script runs a benchmark and performs GPU PROFILING
# 
# 1st arg: data-set/query
# 2nd arg: number of joins (permutations read from file with # perms)
# 3rd arg: additional args to pass on to python (usually --gpu to run on GPU)

echo "Benchmarking $1 ..."

QUERY=$1

while read PERM; do
    
    LOG_FILE="results/ncu/job/"$PERM".csv"
    echo "saving to '"$LOG_FILE"'"

    ncu -f --csv \
        --section MemoryWorkloadAnalysis --section InstructionStats --section SpeedOfLight \
        --metrics "regex:^dram__bytes_(read|write).sum$" \
        --log-file $LOG_FILE \
        python3 main.py run $QUERY $PERM --GPU

done <scripts/perms/$2.csv
