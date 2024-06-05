#!/bin/bash

# Start process.py in the background

python app.py &
FILE1_PID=$!

python pull-service.py 2>&1 &
FILE2_PID=$!



cleanup() {
    echo "Stopping services..."
    kill $FILE1_PID $FILE2_PID  # Kill both processes
    exit
}


# Trap termination signals
trap cleanup INT TERM


while true; do
    if ! kill -0 $FILE2_PID >/dev/null 2>&1; then
        echo "pull-service.py has exited."
        exit 1
    fi
    sleep 1
done
