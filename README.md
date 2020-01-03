# vultrFirewallDynamicDNS

| **CREDITS**|
| --- | --- |
| **MBRCTV** | https://github.com/MBRCTV/VultrFirewallDynamicDNS |
| **andyjsmith** | https://github.com/andyjsmith/Vultr-Dynamic-DNS |

**Vultr API Referenfe**: https://www.vultr.com/api/

**1.** Enable Vultr API in **Account** Menu, API Option.
**2.** Get **Group IDs** you want to always update the IP address
**3.** Inside the Group IDs you want to update, add the rules and insert a note that will be used to update the rules automatically 
**4.** Rename **sample.ddns_config.json** to **ddns_config.json**
**5.** Setup your Vultr API Key in: **api_key**
**6.** Setup your Vultr **Firewall Group IDs** in: **firewallgroupids** ["XXXXX","YYYYY","ZZZZZ"]
**7.** Set **Server Mode** to yes if you do not need to run in using ddns, to add the server IP to firewall, remember to allow this IP address to use the API Key
**8.** Set **ddns_domain** the host you want to resolve

Create a task in Task Scheduler to run whatever time interval you want. 

Follow the Microsoft guide for basic task creation.

Open Task Scheduler and click "Create Task...".
Give it a name and create a new trigger.
Click "Daily". Under "Advanced Settings" click to repeat the task every 30 minutes and change "for a duration of" to "Indefinitely".
Add a new action to start a program and browse to your Python executable. Add the ddns.py script as an argument.

