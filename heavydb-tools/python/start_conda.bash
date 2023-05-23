if [[ -n "$( docker ps -a -q -f name=mm_conda_heavydb )" ]]; then
  echo 'Stopping and removing existing mm_conda_heavydb...'
  ./stop_conda.bash
  docker container rm mm_conda_heavydb
fi

docker run \
    --name mm_conda_heavydb \
    --network=mm_heavydb_network \
    -v /workspace/mmatusovic/projects/heavydb-tools/python/scripts:/root/scripts \
    -i -t mmatusovic/conda_heavydb /bin/bash
