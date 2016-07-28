#!/bin/bash
./run_task.py -n "cctv3_test" -i "udp://235.1.1.2:48880" -h 10:10:15 \
    -t 640x480:318:main:3.1:32:/mnt/remote/r4/wd_r4/test/cctv3_test/350 \
    -t 852x480:568:main:3.1:32:/mnt/remote/r4/wd_r4/test/cctv3_test/600 \
    -t 1280x480:1072:high:5.1:128:/mnt/remote/r4/wd_r4/test/cctv3_test/1200 \
#                -v debug
