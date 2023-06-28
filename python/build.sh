ENV=${1:-"run"}

docker build -t mmatusovic/python:dev -f Dockerfile.dev .

if [ $ENV = 'run' ]; then
    docker build -t mmatusovic/python:run -f Dockerfile.run .
fi;
