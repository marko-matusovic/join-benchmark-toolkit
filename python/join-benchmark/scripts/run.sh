# Run from project root, not from scripts folder. So from scripts/../ which is join-benchmark folder
# 
# 1st arg: the file to run (in set: "out", "in_detail", ...)
# 2nd arg: job or ssb or with query
#       if only "ssb" or "job" is passed all queries will be run after each other, 
#       if a specifi cquery is given, like "job/20a", run only that query.
# 3rd arg: passed to the script

if [ $2 = 'ssb' ]; then
    $1 ssb/q11 1 ${@:3}
    $1 ssb/q12 1 ${@:3}
    $1 ssb/q13 1 ${@:3}
    $1 ssb/q21 3 ${@:3}
    $1 ssb/q31 3 ${@:3}
    $1 ssb/q41 4 ${@:3}
fi;

if [ $2 = "ssb/q11" ]; then
    $1 ssb/q11 1 ${@:3}
fi;
if [ $2 = "ssb/q12" ]; then
    $1 ssb/q12 1 ${@:3}
fi;
if [ $2 = "ssb/q13" ]; then
    $1 ssb/q13 1 ${@:3}
fi;
if [ $2 = "ssb/q21" ]; then
    $1 ssb/q21 3 ${@:3}
fi;
if [ $2 = "ssb/q31" ]; then
    $1 ssb/q31 3 ${@:3}
fi;
if [ $2 = "ssb/q41" ]; then
    $1 ssb/q41 4 ${@:3}
fi;




if [ $2 = 'job' ]; then
    $1 job/1b 5 ${@:3}
    $1 job/2a 5 ${@:3}
    $1 job/20a 12 ${@:3}
    $1 job/22a 16 ${@:3}
    $1 job/28a 23 ${@:3}
    $1 job/30a 21 ${@:3}
fi;

if [ $2 = 'job/1b' ]; then
    $1 job/1b 5 ${@:3}
fi;
if [ $2 = 'job/2a' ]; then
    $1 job/2a 5 ${@:3}
fi;
if [ $2 = 'job/20a' ]; then
    $1 job/20a 12 ${@:3}
fi;
if [ $2 = 'job/22a' ]; then
    $1 job/22a 16 ${@:3}
fi;
if [ $2 = 'job/28a' ]; then
    $1 job/28a 23 ${@:3}
fi;
if [ $2 = 'job/30a' ]; then
    $1 job/30a 21 ${@:3}
fi;
