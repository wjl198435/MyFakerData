#!/bin/sh
# nohup command > myout.file 2>&1 &
nohup  python3  dbManager.py >  faker_iot_data.log 2>&1 &
