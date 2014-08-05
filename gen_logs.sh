#!/bin/bash

if [ ! -d logs/ ]; then
    mkdir logs
fi
cd logs/

MASTER_LOG="master"
for STATUS_CODE in `cat status_codes.txt`; do
    HOUR="02"
    SECOND="00"
    for MINUTE in `seq 1 59`; do
        if [ ${#MINUTE} -lt 2 ]; then
            MINUTE=0${MINUTE}
        fi
        TIME_STAMP=04/Aug/2014:${HOUR}:${MINUTE}:${SECOND}
        COUNT=`echo $RANDOM % 100 + 1 | bc`
        for j in `seq 1 ${COUNT}`; do
            echo "23.65.150.10 - - [${TIME_STAMP}] \"POST /wordpress3/wp-admin/admin-ajax.php HTTP/1.1\" ${STATUS_CODE} 2 \"http://www.example.com/wordpress3/wp-admin/post-new.php\" \"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.25 Safari/534.3\"" >> $MASTER_LOG
        done
    done
done
for i in `seq 1 1000`; do
    cp master log_${i}.log
done
