import subprocess
import json
import socket
import os


def save_disks():
    disk_array = []
    cmd = "lsblk -dno name,type,size --json"
    cmd_out = subprocess.check_output(cmd, shell=True)
    # Load into python types
    python_readable = json.loads(cmd_out)
    for disk in python_readable["blockdevices"]:
        if disk["type"] == "disk":
            #print(disk["name"])
            disk_s3_name = f"{disk['name']}_{disk['size']}"
            disk_array.append(disk_s3_name)
    return disk_array
                 
def get_ipmi_addr():
    cmd = """ipmitool lan print | grep -E 'IP Address.*:\ 10.21' | awk -F: '{print $NF}' """
    ipmi_addr = subprocess.run(cmd, shell=True, capture_output=True, universal_newlines=True)

    return ipmi_addr.stdout.strip()

    #ipmitool_cmd = ["/usr/bin/ipmitool", "lan", "print"] 
    #grep_cmd = [ "grep", "-E", "IP Address.*:\ 10.21" ]
    #awk_cmd = [ "awk", "-F:", "{print $NF}" ]
    
    #ipmi_process = subprocess.Popen(ipmitool_cmd, stdout=subprocess.PIPE, text=True)
    #grep_process = subprocess.Popen(grep_cmd, stdin=ipmi_process.stdout, stdout=subprocess.PIPE, text=True)
    #awk_process = subprocess.Popen(awk_cmd, stdin=grep_process.stdout, stdout=subprocess.PIPE, text=True)
    # Run the three processes.
    #output, error = awk_process.communicate()



def get_ssh_ip_addr():
    # Loop over hostname -I output and print the entire line if it contains "10.21.30"
    cmd = """for i in $(hostname -I ); do echo $i | awk -F. '/10.21.30/{ print $0 }' ; done"""
    ip_addr = subprocess.run(cmd, shell=True, capture_output=True, universal_newlines=True)
    return ip_addr.stdout.strip()

print(get_ssh_ip_addr())
print(get_ipmi_addr())
print(socket.gethostname())

#disk_array = save_disks()
#print(disk_array)


#client = Minio('172.22.1.14:9000', access_key = 'onram', secret_key = '123qwe123qwe', secure=False)

#hostname = os.uname().nodename.split('.')[0].lower()

# print(hostname)
# if not client.bucket_exists(f"{hostname}"):
#     client.make_bucket(f"{hostname}")
#     print(f"{hostname} created")
# else:
#     print(f"{hostname} exists")

# buckets = client.list_buckets()
# for bucket in buckets:
#     print(bucket.name, bucket.creation_date)

exit