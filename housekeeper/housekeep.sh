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

finish_client(){
    local hostname="$1"
    json_string=$(
    jq --null-input \
        --arg power_state "finished" \
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
    elif [[ $1 == "housekeep" ]]; then
        echo $(curl -s http://onram.enginit.se:5000/data/housekeeping | jq '.[]' )
    elif [[ $1 == "finished" ]]; then
        echo $(curl -s http://onram.enginit.se:5000/data | jq '.[] | select(.power_state=="finished")')
    fi
}

down_hosts(){
    for host in $(get_hosts up | jq .hostname | tr -d '"'); do
        ping -q -w 1 ${host} &> /dev/null ; exit_code=$?

        if [[ $exit_code != 0 ]]; then
            stop_client ${host}
            echo "${host} is now down"
        fi
    done
}


finish_hosts(){
    for i in $(get_hosts housekeep | jq .hostname | tr -d '"'); do
        finish_client $i
        echo "${host} is now finished"
    done
}

# Starting clean up
echo "Housekeeping: started $(get_date_time)"
echo  "Cleaning up hosts that are set to up" 
down_hosts
echo "Finishing old hosts"
finish_hosts
echo "Housekeeping: ended $(get_date_time)"
