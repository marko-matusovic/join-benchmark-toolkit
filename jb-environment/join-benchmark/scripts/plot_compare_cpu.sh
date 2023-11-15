
QUERY=$1
NUM_JOINS=$2

EXPR=$(seq -s "*" $NUM_JOINS)"1"
NUM_COMB=$(bc -e $EXPR)

python3 benchmark/util/plot_compare_cpu.py $QUERY -m bin_size -b $NUM_COMB
