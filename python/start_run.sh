./build.sh run

ext="run_"${1:-"main"}

if [[ -n "$( docker ps -a -q -f name=mmatusovic_python_$ext )" ]]; then
    ./stop.sh $ext
fi

echo "Creating new container"

docker run \
    --name mmatusovic_python_$ext \
    -ti \
    --memory 32GB \
    --privileged \
    --runtime=nvidia \
    -e NVIDIA_VISIBLE_DEVICES=0 \
    -d --gpus '"device=0"' \
    -v "/workspace/mmatusovic/projects/python/join-benchmark/results:/app/join-benchmark/results" \
    -v "/workspace/mmatusovic/projects/python/join-benchmark/data:/app/join-benchmark/data" \
    mmatusovic/python:run

docker exec -it mmatusovic_python_$ext bash
