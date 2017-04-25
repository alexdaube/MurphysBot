#!/bin/bash

robot_lanch_home=/home/murphy/projects/glo
log_path=/home/murphy/Desktop/robot_logs/
log_file=${log_path}$(date).log



start() {
    touch "${log_file}"
	echo starting robot at: $(date) &>> "${log_file}"
	cd ${robot_lanch_home}
	./robot_main.py &>> "${log_file}" &
}

stop() {
	killall robot_main.py
	echo stopping robot at: $date >> "${log_file}"
}

status() {
	ps cax | grep robot_main.py > /dev/null
	if [ $? -eq 0 ]; then
  		echo "Process is running."
	else
  		echo "Process is not running."
	fi
}

case "$1" in 
    start)
	start
       ;;
    stop)
	stop
       ;;
    restart)
	stop
	start
       ;;
    status)
	status
       ;;
    *)
       echo "Usage: $0 {start|stop|status|restart}"
esac




