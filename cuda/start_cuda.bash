if [[ -n "$( docker ps -a -q -f name=mm_heavydb )" ]]; then
    echo "Resuming container"
else
    echo "Creating new container"
    ./make_cuda.bash
fi

docker container start mm_cuda
docker exec -it mm_cuda bash
