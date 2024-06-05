#!/bin/bash

# Start process.py with Gunicorn in the background
gunicorn -b 0.0.0.0:5000 process:app &
PROCESS_PID=$!

# Start main_server.py with Gunicorn in the background
gunicorn -b 0.0.0.0:4000 main_server:app &
MAIN_SERVER_PID=$!

# Start app.py with Gunicorn in the background
gunicorn -b 0.0.0.0:3000 app:app &
APP_PID=$!


# Start pull-service.py in the foreground (assuming it should run in the foreground)
python pull-service.py &
PULL_SERVICE_PID=$!

cleanup() {
    echo "Stopping services..."
    kill $PROCESS_PID $MAIN_SERVER_PID $APP_PID $PULL_SERVICE_PID
    exit
}

# Trap termination signals
trap cleanup INT TERM

# Monitor all processes
while true; do
    if ! kill -0 $PROCESS_PID >/dev/null 2>&1; then
        echo "process.py has exited."
        exit 1
    fi
    if ! kill -0 $MAIN_SERVER_PID >/dev/null 2>&1; then
        echo "main_server.py has exited."
        exit 1
    fi
    if ! kill -0 $APP_PID >/dev/null 2>&1; then
        echo "app.py has exited."
        exit 1
    fi
    if ! kill -0 $PULL_SERVICE_PID >/dev/null 2>&1; then
        echo "pull-service.py has exited."
        exit 1
    fi
    sleep 1
done
