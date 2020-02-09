#!/bin/sh

PID_FILE="/tmp/one_time_sync.CONFIG_NAME.pid" # Must be same as the one in sample.ini

if [ -f ${PID_FILE} ]; then
	kill -SIGTERM `cat ${PID_FILE}`
fi
