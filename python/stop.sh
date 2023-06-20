ext=${1:-"*"}

if [[ ! $(docker container ls -q --filter name="mmatusovic_python_$ext") ]]; then
    echo "No containers matching \"mmatusovic_python_$ext\" running."
else
    echo Stopping containers ...
    docker container stop $(docker container ls -q --filter name="mmatusovic_python_$ext")

    echo Removing containers ...
    docker container rm $(docker container ls -a -q --filter name="mmatusovic_python_$ext")
fi