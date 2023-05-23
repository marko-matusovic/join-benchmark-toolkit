ext=${1:-"*"}

echo Stopping containers ...
docker container stop $(docker container ls -q --filter name="mmatusovic_python_$ext")

echo Removing containers ...
docker container rm $(docker container ls -a -q --filter name="mmatusovic_python_$ext")
