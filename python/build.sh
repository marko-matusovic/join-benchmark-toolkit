ENV=${1:-"all"}

if [ $ENV = 'dev' ]; then
    docker build -t mmatusovic/python:dev -f Dockerfile.dev .
fi;

if [ $ENV = 'run' ]; then
    docker build -t mmatusovic/python:run -f Dockerfile.run .
fi;

if [ $ENV = 'all' ]; then
    docker build -t mmatusovic/python:dev -f Dockerfile.dev .
    docker build -t mmatusovic/python:run -f Dockerfile.run .
fi;

