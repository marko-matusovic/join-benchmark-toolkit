#! /bin/bash

PROJECT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DBS=${1:-'all'}
SCALE=${2:-'10'}
TARGET_DIR=${3:-$PROJECT_DIR'/jb-environment/join-benchmark/data'}

# TPC-DS
function tpcds() {
    cd $PROJECT_DIR/tpcds-kit
    rm -rf tmp
    mkdir tmp
    cd tmp
    mkdir tables

    cd $PROJECT_DIR/tpcds-kit/tools
    make OS=LINUX

    ./dsdgen \
        -scale $SCALE \
        -force Y \
        -dir ../tmp/tables

    sleep 3

    cd $TARGET_DIR/tpcds
    rm -rf tables
    mkdir tables

    mv $PROJECT_DIR/tpcds-kit/tmp/tables/* tables
    rm -rf $PROJECT_DIR/tpcds-kit/tmp/*
    echo "scale: $SCALE" > tables/scale.txt
}

# JOB
function job() {
    cd $PROJECT_DIR/imdb-db-tool
    ./download_tables.sh

    cd $TARGET_DIR/job
    mkdir tables
    rm -rf tables/*

    mv $PROJECT_DIR/imdb-db-tool/tables/*.csv tables
    rm -rf $PROJECT_DIR/imdb-db-tool/tables/*
}

# SSB
function ssb() {
    cd $PROJECT_DIR/ssb-dbgen

    cmake -DCSV_OUTPUT_FORMAT=ON .
    cmake --build .
    
    rm -rf *.tbl
    ./dbgen -v -s $SCALE

    cd $TARGET_DIR/ssb

    rm -rf tables
    mkdir tables
    mv $PROJECT_DIR/ssb-dbgen/*.tbl tables
    mv tables/date.tbl tables/ddate.tbl
    rm -rf $PROJECT_DIR/ssb-dbgen/*.tbl
    echo "scale: $SCALE" > tables/scale.txt
}

if [[ $DBS == "all" ]]; then
    # Trigger all 3 jobs at once
    echo "Generating TPC-DS, and SSB at scale $SCALE, and downloading JOB"
    ssb & \
    tpcds & \
    job & \
    wait
fi;

if [[ $DBS == "job" ]]; then
    # Trigger all 3 jobs at once
    echo "Generating JOB"
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
