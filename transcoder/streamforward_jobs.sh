#!/bin/bash
./do_jobs.py -Y "ffmpeg -nhb -i 'udp://236.114.1.1:10001?overrun_nonfatal=1&fifo_size=10000000' -map p:3801 -c copy -f mpegts udp://192.168.109.200:50001"