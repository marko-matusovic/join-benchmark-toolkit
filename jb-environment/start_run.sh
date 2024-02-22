./build.sh run

ext="run_"${1:-"main"}

if [[ -n "$( docker ps -a -q -f name=mmatusovic_python_$ext )" ]]; then
    ./stop.sh $ext
fi

echo "Purging stats"
rm -rf /workspace/mmatusovic/msc-wis-test-environment/jb-environment/join-benchmark/data/**/stats/*

echo "Creating new container"

docker run \
    --name mmatusovic_python_$ext \
    -ti \
    --memory 32GB \
    --privileged \
    --runtime=nvidia \
    -e NVIDIA_VISIBLE_DEVICES=0 \
    -d --gpus 'all' \
    -v "/workspace/mmatusovic/msc-wis-test-environment/jb-environment/join-benchmark/results:/app/join-benchmark/results" \
    -v "/workspace/mmatusovic/msc-wis-test-environment/jb-environment/join-benchmark/data:/app/join-benchmark/data" \
    mmatusovic/python:run

    # -d --gpus '"device=0"' \
    
docker exec -it mmatusovic_python_$ext bash
