./build.sh dev

ext="dev_"${1:-"main"}

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
    -v "/workspace/mmatusovic/projects/python/join-benchmark:/app/join-benchmark" \
    mmatusovic/python:dev

docker exec -it mmatusovic_python_$ext bash
