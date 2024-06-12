#!/bin/bash
# Usage: ./wait-for-it.sh hostname:port [-t timeout] [-- command args]
# Forked from https://github.com/vishnubob/wait-for-it

# Defaults
timeout=120
cmd=""

# Parse arguments
while [[ $# -gt 0 ]]
do
    case "$1" in
        *:* )
        hostport=(${1//:/ })
        host=${hostport[0]}
        port=${hostport[1]}
        shift 1
        ;;
        -t )
        timeout="$2"
        shift 2
        ;;
        -- )
        cmd="$@"
        break
        ;;
        * )
        echo "Invalid argument: $1"
        exit 1
        ;;
    esac
done

# Validate arguments
if [[ -z $host || -z $port ]]
then
    echo "Usage: $0 hostname:port [-t timeout] [-- command args]"
    exit 1
fi

echo "Waiting for $host:$port to become available..."

# Start time
start_time=$(date +%s)

# Wait for the service to become available
while :
do
    nc -z -w 1 $host $port 2>/dev/null && break
    sleep 1
    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))
    if [[ $elapsed_time -ge $timeout ]]
    then
        echo "Timed out waiting for $host:$port"
        exit 1
    fi
done

# Execute the command
if [[ -n $cmd ]]
then
    echo "Service $host:$port is available, executing command: $cmd"
    exec $cmd
else
    echo "Service $host:$port is available"
fi
