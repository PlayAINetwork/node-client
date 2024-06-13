#!/bin/bash

# Start the task getting service in the background



python pull-service.py &
FILE1_PID=$!


# Start rest endpoint for health in foreground

python app.py


cleanup() {
    echo "Stopping services..."
    kill $FILE1_PID   # Kill processes
    exit
}


# Trap termination signals together
trap cleanup INT TERM


while true; do
    if ! kill -0 $FILE1_PID >/dev/null 2>&1; then
        echo "pull-service.py has exited."
        exit 1
    fi
    sleep 1
done
