ext=${1:-"0"}

if [[ -n "$( docker ps -a -q -f name=mm_python_$ext )" ]]; then
    echo "Recreating existing container"
    ./stop_py.bash $ext
else
    echo "Creating new container"
fi

docker run \
    --name mm_python_$ext \
    -ti \
    --memory 32GB \
    --privileged \
    --runtime=nvidia \
    -e NVIDIA_VISIBLE_DEVICES=0 \
    -d --gpus '"device=0"' \
    -v "/workspace/mmatusovic/projects/python/join-benchmark:/app/join-benchmark" \
    mm_python_img

docker exec -it mm_python_$ext bash

