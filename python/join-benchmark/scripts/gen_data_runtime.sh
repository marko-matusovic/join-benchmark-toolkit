# Run from project root, not from scripts folder. So from scripts/../ which is join-benchmark folder
# 
# 1st arg: db_set to use to gen data [ssb, job]

DB_SET=$1

if [ $2 = 'ssb' ]; then
    $1 ssb/q11 1 ${@:3}
    $1 ssb/q12 1 ${@:3}
    $1 ssb/q13 1 ${@:3}
    $1 ssb/q21 3 ${@:3}
    $1 ssb/q31 3 ${@:3}
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

