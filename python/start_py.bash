ext=${1:-"0"}

if [[ -n "$( docker ps -a -q -f name=mm_python_$ext )" ]]; then
    echo "Resuming container"
else
    echo "Creating new container"
    ./make_py.bash
fi

docker container start mm_python_$ext
docker exec -it mm_python_$ext bash
