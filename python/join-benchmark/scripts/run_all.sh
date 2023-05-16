if [ $2 = 'ssb' ]; then 
    ./scripts/$1.sh ssb/q11 1
    ./scripts/$1.sh ssb/q12 1
    ./scripts/$1.sh ssb/q13 1
    ./scripts/$1.sh ssb/q21 3
    ./scripts/$1.sh ssb/q31 3
    ./scripts/$1.sh ssb/q41 4
fi;

if [ $2 = 'job' ]; then 
    ./scripts/$1.sh job/1b 5
    ./scripts/$1.sh job/2a 5
    ./scripts/$1.sh job/20a 12
    ./scripts/$1.sh job/22a 16
    ./scripts/$1.sh job/28a 23
    ./scripts/$1.sh job/30a 21
fi;