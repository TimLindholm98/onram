#!/bin/bash

api_endpoint=""
api_port=""


# Get short easy to look at values. 
get_cpu_name(){
    echo "$(lscpu --json | jq '.lscpu[] | select(.field=="Model name:") | .data' | tr -d '"')"
}
get_threads(){
    echo "$(nproc)"
}
get_ram_total(){
    echo "$(lsmem --json | jq .memory[].size | tr -d '"')"
}
get_ram_sticks(){
    echo "$(dmidecode -t memory | grep -E "^\sSize\:.*\sGB$" | awk -F: '{print $NF}' | tr -d [:blank:] | uniq -c | awk '{print $1}')"
}
get_hostname(){
    echo "$(hostname)"
}
get_ip_addr(){
    echo "$(for i in $(hostname -I); do echo $i | awk -F. '/10.21.30/{print $0}' ; done)"
}
get_ipmi_addr(){
    echo "$(ipmitool lan print | grep "IP Address  " | cut -d: -f2 | tr -d [:blank:])"
}
get_all_nvme(){
    echo "$(lsblk -n -o name,size,rota,type /dev/nvme* 2> /dev/null | awk '$NF ~ /disk/{print $1 "," $2 "," $3}' |  awk -F, '$NF ~ /0/{print $1 "," $2}' | wc -l)"
}
get_all_ssd(){
    echo "$(lsblk -n -o name,size,rota,type /dev/sd* 2> /dev/null | awk '$NF ~ /disk/{print $1 "," $2 "," $3}' |  awk -F, '$NF ~ /0/{print $1 "," $2}' | wc -l)"
}
get_all_hdd(){
    echo "$(lsblk -n -o name,size,rota,type /dev/sd* 2> /dev/null | awk '$NF ~ /disk/{print $1 "," $2 "," $3}' |  awk -F, '$NF ~ /1/{print $1 "," $2}' | wc -l)"
}


# More information
list_ram_sticks(){
    echo "$(dmidecode -t memory | grep -E "^\sSize\:.*\sGB$" | awk -F: '{print $NF}' | tr -d [:blank:] | uniq -c | awk '{print $1 "," $2}')"
}
list_all_nvme(){
    echo "$(lsblk -n -o name,size,rota,type /dev/nvme* 2> /dev/null | awk '$NF ~ /disk/{print $1 "," $2 "," $3}' |  awk -F, '$NF ~ /0/{print $1 "," $2}')"
}
list_all_ssd(){
    echo "$(lsblk -n -o name,size,rota,type /dev/sd* 2> /dev/null | awk '$NF ~ /disk/{print $1 "," $2 "," $3}' |  awk -F, '$NF ~ /0/{print $1 "," $2}')"
}
list_all_hdd(){
    echo "$(lsblk -n -o name,size,rota,type /dev/sd* 2> /dev/null | awk '$NF ~ /disk/{print $1 "," $2 "," $3}' |  awk -F, '$NF ~ /1/{print $1 "," $2}')"
}

# https://stackoverflow.com/questions/48470049/build-a-json-string-with-bash-variables

# Generating a JSON string (https://stackoverflow.com/a/68591585)
json_string=$(
  jq --null-input \
    --arg hostname "$(get_hostname)" \
    --arg ip "$(get_ip_addr)" \
    --arg ipmi "$(get_ipmi_addr)" \
    --arg cpu "$(get_cpu_name)" \
    --arg threads "$(get_threads)" \
    --arg ram "$(get_ram_total)" \
    --arg ram_sticks "$(get_ram_sticks)" \
    --arg nvme "$(get_all_nvme)" \
    --arg ssd "$(get_all_ssd)" \
    --arg hdd "$(get_all_hdd)" \
    '$ARGS.named'
)

printf "%s" "$json_string" > /tmp/onram_client.json

# curl -X POST -H "Content-Type: application/json" -d @FILENAME DESTINATION

curl --header "Content-Type: application/json" \
  --request "DELETE" \
  http://10.21.30.200:5000/data/$(get_hostname)

curl --header "Content-Type: application/json" \
  --request "POST" \
  --data "@/tmp/onram_client.json" \
  http://10.21.30.200:5000/data
