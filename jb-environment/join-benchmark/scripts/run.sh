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

# job/1a 5
# job/1b 5
# job/1c 5
# job/1d 5
# job/2a 5
# job/2b 5
# job/2c 5
# job/2d 5
# job/3a 4
# job/3b 4
# job/3c 4
# job/4a 5
# job/4b 5
# job/4c 5
# job/5a 5
# job/5b 5
# job/5c 5
# job/6a 5
# job/6b 5
# job/6c 5
# job/6d 5
# job/6e 5
# job/6f 5
# job/7b 11
# job/8a 7
# job/8b 8
# job/8c 7
# job/8d 7
# job/9a 9
# job/9b 9
# job/9c 9
# job/9d 9
# job/10a 7
# job/10b 7
# job/10c 7
# job/11a 10
# job/11b 10
# job/11c 10
# job/11d 10
# job/12a 8
# job/12b 8
# job/12c 8
# job/13a 11
# job/13b 11
# job/13c 11
# job/13d 11
# job/14a 10
# job/14b 10
# job/14c 10
# job/15a 14
# job/15b 14
# job/15c 14
# job/15d 14
# job/16a 11
# job/16b 11
# job/16c 11
# job/16d 11
# job/17a 9
# job/17b 9
# job/17c 9
# job/17d 9
# job/17e 9
# job/17f 9
# job/18a 9
# job/18b 9
# job/18c 9
# job/19a 13
# job/19b 13
# job/19c 13
# job/19d 13
# job/20a 12
# job/20b 12
# job/20c 12
# job/21a 14
# job/21b 14
# job/21c 14
# job/22a 16
# job/22b 16
# job/22c 16
# job/22d 16
# job/23a 16
# job/23b 16
# job/23c 16
# job/24a 18
# job/24b 18
# job/25a 14
# job/25b 14
# job/25c 14
# job/26a 17
# job/26b 17
# job/26c 17
# job/27a 21
# job/27b 21
# job/27c 21
# job/28a 23
# job/28b 23
# job/28c 23
# job/29a 28
# job/29b 28
# job/29c 28
# job/30a 21
# job/30b 21
# job/30c 21
# job/31a 20
# job/31b 20
# job/31c 20
# job/32a 3
# job/32b 3
# job/33a 3
# job/33b 3
# job/33c 3





if [ $2 = 'tpcds' ]; then
    $1 tpcds/query_3 2 ${@:3}
    $1 tpcds/query_6 4 ${@:3}
    $1 tpcds/query_7 4 ${@:3}
    $1 tpcds/query_12 2 ${@:3}
    $1 tpcds/query_15 3 ${@:3}
    $1 tpcds/query_17 7 ${@:3}
    $1 tpcds/query_18 6 ${@:3}
    $1 tpcds/query_19 5 ${@:3}
    $1 tpcds/query_20 2 ${@:3}
    # $1 tpcds/query_ ${@:3}
fi;
