#!/bin/bash

db_volume=${1:-"default"}

if [ -d "/workspace/mmatusovic/heavyai-storage/$db_volume" ]; then
  echo "Using db sotrage '$db_volume'."
else
  echo "Creating new db storage named '$db_volume'."
  mkdir /workspace/mmatusovic/heavyai-storage/$db_volume
  cat /workspace/mmatusovic/heavyai-storage/heavy.conf > /workspace/mmatusovic/heavyai-storage/$db_volume/heavy.conf
fi

# result=$( docker ps -a -q -f name="mm_heavydb" )
# if [[ -n "$result" ]]; then
if [[ -n "$( docker ps -a -q -f name=mm_heavydb )" ]]; then
  echo 'Stopping and removing existing mm_heavydb...'
  ./stop_db.bash
  docker container rm mm_heavydb
fi

echo 'Running new mm_heavydb...'

docker run \
    --name mm_heavydb \
    --network=mm_heavydb_network \
    --privileged \
    -m 32g \
    -d --gpus '"device=0"' \
    -v "/workspace/mmatusovic/heavyai-storage/$db_volume:/var/lib/heavyai" \
    -p 6273-6278:6273-6278 \
    mmatusovic/heavydb_profiler:latest

echo 'Entering bash...'
docker exec -it mm_heavydb bash
