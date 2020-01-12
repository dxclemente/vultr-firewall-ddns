import requests
import time
import json
import socket

# Import the values from the configuration file
with open("ddns_config.json") as config_file:
    config = json.load(config_file)  # Convert JSON to Python

firewallgroupids = config["firewallgroupids"]
api_key = config["api_key"]
user = config["user"]
server_mode = config["server_mode"]
ddns_domain = config["ddns_domain"]

# Get the public IP of the server
if server_mode == "no":
    # your os sends out a dns query
    ip = socket.gethostbyname(ddns_domain)
else:
    ip = requests.get("https://ip.42.pl/raw").text

for list_rules in firewallgroupids:
    firewallgroup = list_rules
    #print(list_rules)

    # Get the list of Firewall records from Vultr to update the ones with user setup in config file
    time.sleep(1) # 1 second waiting before making requests, to avoid reach Vultr rate hits
    url = "https://api.vultr.com/v1/firewall/rule_list?FIREWALLGROUPID=" + firewallgroup + "&direction=in&ip_type=v4"
    raw_rules = requests.get(url, headers={"API-Key": api_key}).json()

    # Make a new varible with the vultr ip
    v_ip = ""
    for rule in raw_rules:
        if raw_rules[rule]["notes"] == user:
            v_rulenumber = raw_rules[rule]["rulenumber"]
            v_notes = raw_rules[rule]["notes"]
            v_port = raw_rules[rule]["port"]
            v_protocol = raw_rules[rule]["protocol"]
            v_subnet_size = raw_rules[rule]["subnet_size"]
            v_subnet = raw_rules[rule]["subnet"]
            v_ip = v_subnet
            #print(v_ip + ":" + v_port)
            needsUpdated = False
            if firewallgroup + v_ip + ":" + v_port != firewallgroup + ip + ":" + v_port:
                needsUpdated = True
            #print(needsUpdated)

            if len(v_ip) == 0:
                print("Configuration error, no ip found for this user.")
                quit()

            # Cancel if the IP has not changed
            if not needsUpdated:
                print("For firewall group rule " + list_rules 
                      + " your IP:Port is: " + ip +":"+ v_port 
                      + ". Rule has not changed and have not been updated.")
            else:
                for rule in raw_rules:
                    print("Your IP for the rule " + list_rules + " has changed since last checking"
                          + ". Old IP on Vultr: " + v_ip + ":" + v_port
                          + " Current Device IP: " + ip + ":" + v_port)

                    # Remove old Firewall rule
                    time.sleep(1) # 1 second waiting before making requests, to avoid reach Vultr rate hits
                    payload = {"FIREWALLGROUPID": list_rules, "rulenumber": v_rulenumber}
                    response = requests.post("https://api.vultr.com/v1/firewall/rule_delete",
                                            data=payload, headers={"API-Key": api_key})
                    if response.status_code == 200:
                        print("Current rule for " + v_ip + ":" + v_port 
                              + " for group id " + list_rules + " has been deleted")
                    else:
                        print("Deleting port:" + v_port 
                              + " in rule id: " + firewallgroup)

                    # Update the rule in Vultr with the new IP address
                    time.sleep(1) # 1 second waiting before making requests, to avoid reach Vultr rate hits
                    payload = {"FIREWALLGROUPID": firewallgroup,
                            "direction": "in",
                                            "ip_type": "v4",
                                            "protocol": v_protocol,
                                            "subnet": ip,
                                            "subnet_size": v_subnet_size,
                                            "port": v_port,
                                            "notes": v_notes}
                    response = requests.post("https://api.vultr.com/v1/firewall/rule_create",
                                            data=payload, headers={"API-Key": api_key})
                    if response.status_code == 200:
                        print("user " + user + " has been updated to " + ip + ":" + v_port)
                        break
                    else:
                        print("Error adding rule")