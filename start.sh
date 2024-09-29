#!/bin/sh
export PYTHONUNBUFFERED=1
nohup python3 app.py &

sleep 1
tail -f nohup.out

