docker run \
    --name mm_python \
    -ti \
    --runtime=nvidia \
    -e NVIDIA_VISIBLE_DEVICES=0 \
    -d --gpus '"device=0"' \
    -v "/workspace/mmatusovic/projects/python/volume:/root" \
    mm_python_img

docker exec -it mm_python bash
