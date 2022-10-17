#!/bin/bash
# wait-for-grid.sh

set -e

cmd="$@"

while ! curl -sSL "http://selenium-hub:4444/wd/hub/status" 2>&1 \
        | jq -r '.value.ready' 2>&1 | grep "true" >/dev/null; do
    echo 'Waiting for the Grid'
    sleep 1
done
#sleep 10
while ! curl -4 --head  http://loadbalancer | grep "HTTP/1.1 200" 2>&1 > /dev/null; do
    echo 'Waiting for frontend to be up...'
    sleep 1
done
>&2 echo "Selenium Grid is up - executing tests"
exec $cmd