ext=${1:-"0"}

if [[ -n "$( docker ps -a -q -f name=mm_python_$ext )" ]]; then
    echo "Recreating existing container"
    ./stop_py.bash $ext
else
    echo "Creating new container"
fi

./make_py.bash $ext
