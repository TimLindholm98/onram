#!/bin/bash

api_endpoint="onram.enginit.se"
api_port="5000"


stop_client(){
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
    http://${api_endpoint}:${api_port}/data/power_state/$(get_hostname)
}



if [[ -z "$@" ]]; then
  echo "Please add start or stop as \$1 argument"
elif [[ "$1" == "start" ]]; then
    start_client
elif [[ "$1" == "stop" ]]; then
    stop_client
elif [[ "$1" == "finish" ]]; then
    finish_client
fi
