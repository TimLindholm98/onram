#!/bin/bash

api_endpoint="onram.enginit.se"
api_port="5000"

get_date_time(){
    TZ="Europe/Stockholm"
    echo "$(date '+%Y-%m-%d %H:%M:%S')"
}

stop_client(){
    local hostname="$1"
    json_string=$(
    jq --null-input \
        --arg power_state "down" \
        --arg date_time "$(get_date_time)" \
        '$ARGS.named'
    )
    printf "%s" "$json_string" > /tmp/onram_client.json

    curl --header "Content-Type: application/json" \
    --request "PUT" \
    --data "@/tmp/onram_client.json" \
    http://${api_endpoint}:${api_port}/data/power_state/${hostname}
}

get_hosts(){
    if [[ $1 == "all" ]]; then
        echo $(curl -s http://onram.enginit.se:5000/data | jq . )
    elif [[ $1 == "up" ]]; then
        echo $(curl -s http://onram.enginit.se:5000/data | jq '.[] | select(.power_state=="up")')
    elif [[ $1 == "down" ]]; then
        echo $(curl -s http://onram.enginit.se:5000/data | jq '.[] | select(.power_state=="down")')
    elif [[ $1 == "done" ]]; then
        echo $(curl -s http://onram.enginit.se:5000/data | jq '.[] | select(.power_state=="done")')
    fi
}

down_host(){
    # ping hostname from $1
    # if down stop_client function
    local host="$1"
    ping -q -w 1 ${host} ; exit_code=$?

    if [[ $exit_code != 0 ]]; then
        stop_client ${host}
    fi
    echo "${host} is now down"
}

down_hosts(){
    for i in $(get_hosts up | jq .hostname | tr -d '"'); do
        down_host $i
    done
}


# Starting clean up
echo "Housekeeping: started $(get_date_time)"
down_hosts
echo "Housekeeping: ended $(get_date_time)"
