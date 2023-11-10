PROJECT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DBS=${1:-'all'}
SCALE=${2:-'10'}

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
    cd $PROJECT_DIR/ssb-dbgen

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
    ./dbgen -v -s $SCALE

    cd $PROJECT_DIR/python/join-benchmark/data/ssb

    rm -rf tables
    mkdir tables
    mv $PROJECT_DIR/ssb-dbgen/*.tbl tables
}

if [[ $DBS == "all" ]]; then
    # Trigger all 3 jobs at once
    echo "Generating TPC-DS, and SSB at scale $SCALE"
    ssb & \
    tpcds & \
    wait
fi;

if [[ $DBS == "job" ]]; then
    # Trigger all 3 jobs at once
    echo "Generating JOB at scale $SCALE"
    job
fi;

if [[ $DBS == "ssb" ]]; then
    # Trigger all 3 jobs at once
    echo "Generating SSB at scale $SCALE"
    ssb
fi;

if [[ $DBS == "tpcds" ]]; then
    # Trigger all 3 jobs at once
    echo "Generating TPC-DS at scale $SCALE"
    tpcds
fi;

echo "Done!"
