ext=${1:-"0"}

docker container stop mm_python_$ext
docker container rm mm_python_$ext
