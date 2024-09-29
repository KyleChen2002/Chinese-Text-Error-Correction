#!/bin/sh

PID=`ps -ef|grep 'python app.p[y]' | awk '{print $2}'`
if [ "$PID" == "" ]; then
  echo not run
else
  echo kill $PID
  kill $PID
fi
