#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
cd ..

for file in scripts/query_templates/*; do
    base="${file##*/}"
    new_file="${base/xx/sm}"
    sed 's/XX/sm/g' "$file" > "queries/$new_file"
    new_file="${base/xx/md}"
    sed 's/XX/md/g' "$file" > "queries/$new_file"
    new_file="${base/xx/lg}"
    sed 's/XX/lg/g' "$file" > "queries/$new_file"
done
