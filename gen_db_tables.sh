PROJECT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCALE=${1:-'10'}

# TPC-DS
function tpcds() {
    cd $PROJECT_DIR/tpcds-kit
    mkdir tmp
    cd tmp
    mkdir tables

    cd $PROJECT_DIR/tpcds-kit/tools
    make OS=LINUX

    ./dsdgen \
        -scale $SCALE \
        -force Y \
        -dir ../tmp/tables

    cd $PROJECT_DIR/python/join-benchmark/data/tpcds
    rm -rf tables
    mkdir tables

    mv $PROJECT_DIR/tpcds-kit/tmp/tables/* $PROJECT_DIR/python/join-benchmark/data/tpcds/tables
}

# JOB
function job() {
    # cd $PROJECT_DIR/ssb-dbgen

    # cmake -DCSV_OUTPUT_FORMAT=ON .
    # cmake --build .
    # ./dbgen -v -s 15

    # cd $PROJECT_DIR/python/join-benchmark/data/job

    # rm -rf tables
    # mkdir tables
    # mv $PROJECT_DIR/ssb-dbgen/*.tbl tables
}

# SSB
function ssb() {
    cd $PROJECT_DIR/ssb-dbgen

    cmake -DCSV_OUTPUT_FORMAT=ON .
    cmake --build .
    
    rm -rf *.tbl
    ./dbgen -v -s $(( $SCALE * 2 ))

    cd $PROJECT_DIR/python/join-benchmark/data/ssb

    rm -rf tables
    mkdir tables
    mv $PROJECT_DIR/ssb-dbgen/*.tbl tables
}

# Trigger all 3 jobs at once
echo "Generating TPC-DS, JOB, and SSB at scale $SCALE"

ssb & \
# job & \
tpcds & \
wait

# 
