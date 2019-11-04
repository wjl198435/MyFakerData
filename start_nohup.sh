#!/bin/sh
# nohup command > myout.file 2>&1 &
nohub  python3  MySchema.py >  faker_iot_data.log 2>&1 &
