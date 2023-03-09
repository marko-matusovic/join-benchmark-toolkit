docker run \
    --name mm_cuda \
    -ti \
    --runtime=nvidia \
    -e NVIDIA_VISIBLE_DEVICES=0 \
    -m 32g \
    -d --gpus '"device=0"' \
    -v "/workspace/mmatusovic/projects/cuda/volume:/root" \
    nvidia/cuda:11.8.0-devel-ubuntu20.04

docker exec -it mm_cuda bash
