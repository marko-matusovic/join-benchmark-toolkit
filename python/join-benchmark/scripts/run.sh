# Run from project root, not from scripts folder. So from scripts/../ which is join-benchmark folder
# 
# 1st arg: the file to run (in set: "out", "in_detail", ...)
# 2nd arg: job or ssb or with query
#       if only "ssb" or "job" is passed all queries will be run after each other, 
#       if a specifi cquery is given, like "job/20a", run only that query.
# 3rd arg: passed to the script

if [ $2 = 'ssb' ]; then
    ./scripts/$1.sh ssb/q11 1
    ./scripts/$1.sh ssb/q12 1
    ./scripts/$1.sh ssb/q13 1
    ./scripts/$1.sh ssb/q21 3
    ./scripts/$1.sh ssb/q31 3
    ./scripts/$1.sh ssb/q41 4
fi;

if [ $2 = "ssb/q11" ]; then
    ./scripts/$1.sh ssb/q11 1
fi;
if [ $2 = "ssb/q12" ]; then
    ./scripts/$1.sh ssb/q12 1
fi;
if [ $2 = "ssb/q13" ]; then
    ./scripts/$1.sh ssb/q13 1
fi;
if [ $2 = "ssb/q21" ]; then
    ./scripts/$1.sh ssb/q21 3
fi;
if [ $2 = "ssb/q31" ]; then
    ./scripts/$1.sh ssb/q31 3
fi;
if [ $2 = "ssb/q41" ]; then
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

if [ $2 = 'job/1b' ]; then
    ./scripts/$1.sh job/1b 5
fi;
if [ $2 = 'job/2a' ]; then
    ./scripts/$1.sh job/2a 5
fi;
if [ $2 = 'job/20a' ]; then
    ./scripts/$1.sh job/20a 12
fi;
if [ $2 = 'job/22a' ]; then
    ./scripts/$1.sh job/22a 16
fi;
if [ $2 = 'job/28a' ]; then
    ./scripts/$1.sh job/28a 23
fi;
if [ $2 = 'job/30a' ]; then
    ./scripts/$1.sh job/30a 21
fi;