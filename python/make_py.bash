ext=${1:-"0"}

docker run \
    --name mm_python_$ext \
    -ti \
    --runtime=nvidia \
    -e NVIDIA_VISIBLE_DEVICES=0 \
    -d --gpus '"device=0"' \
    -v "/workspace/mmatusovic/projects/python/volume:/root" \
    mm_python_img

docker exec -it mm_python_$ext bash
