#!/bin/bash

# Reset the ipmi to dhcp
ipmitool lan print | grep "IP Address Source" | grep DHCP ; exit_code=$?
if [ $exit_code -eq 1 ]; then
    ipmitool lan set 1 ipsrc dhcp ; exit_code=$?
    if [ $exit_code -eq 1 ]; then
        echo "Failed to change IPMI interface to DHCP mode"
        exit 1
    fi
fi

# Delete host from onram
curl --header "Content-Type: application/json" \
    --request "GET" \
    http://${api_endpoint}:${api_port}/data/$(get_hostname) ; exit_code=$?
if [ $exit_code -eq 1 ]; then
    all_hosts_json="$(curl --header "Content-Type: application/json" --request "GET" http://${api_endpoint}:${api_port}/data/$(get_hostname))" ; exit_code=$?
    if [ $exit_code -eq 1 ]; then
        echo "Is https://onram.enginit.se:5000 down or not reachable?"
        exit 1
    elif [ $exit_code -eq 0]; then
        printf "${all_hosts_json}" | jq .


