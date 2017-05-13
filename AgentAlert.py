import json
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import smtplib
import os.path
import pickle
import ast

#CHANGEME
empire_apikey=""
empire_url="https://localhost:1337"
gmail_user="shellalerts000@gmail.com"
gmail_password=""
# END OF CHANGEME

if os.path.exists("empire_key"):
    with open("empire_key") as key:
        empire_apikey = key.read
    key.close

if os.path.exists("gmail_password"):
    with open("gmail_password") as password:
        gmail_password = password.read

subject = "New agent"
current_agents = []
recipients = []
gateways = {
        "1": "txt.att.net",
        "2": "tmomail.net",
        "3": "vtext.com",
        "4": "messaging.sprintpcs.com",
        "5": "vmobl.com",
        "6": "mmst5.tracfone.com",
        "7": "mymetropcs.com",
        "8": "myboostmobile.com",
        "9": "mms.cricketwireless.net",
        "10": "ptel.com",
        "11": "text.republicwireless.com",
        "12": "msg.fi.google.com",
        "13": "tms.suncom.com",
        "14": "message.ting.com",
        "15": "email.uscc.net",
        "16": "cingularme.com",
        "17": "cspire1.com",
        "18": "vtext.com"  
}

def get_user_info():
    try:
        while True:
            print("Enter mobile number (1234567890), ctrl+C to quit")
            number = raw_input("> ")
            print("""
Enter your carrier (just the number)
1: AT&T
2: T-Mobile
3: Verizon
4: Sprint
5: Virgin Mobile
6: Tracfone
7: Metro PCS
8: Boost Mobile
9: Cricket
10: Ptel
11: Republic Wireless
12: Google Fi
13: Suncom
14: Ting
15: U.S. Cellular
16: Consumer Cellular
17: C-Spire
18: Page Plus""")        
            carrier_id = raw_input("> ")
            gateway = gateways[carrier_id]
            recipients.append((number, gateway))
    except KeyboardInterrupt:
        pass
    return recipients

def send_email(user, gmail_password, recipient, subject, body):
	gmail_user = user
	gmail_pwd = gmail_password
	FROM = user
	TO = recipient if type(recipient) is list else [recipient]
	SUBJECT = subject
	TEXT = body

	# Prepare actual message
	message = """From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(FROM, TO, message)
		server.close()
		print '[*] successfully sent the mail'
	except:
		print "[*] failed to send mail"


if not os.path.exists("config"):
    print("[*] No config found")
    recipients = get_user_info()
else:
    print("[*] Found config file")
    with open('config') as config:
        recipients=pickle.load(config)
    config.close

if os.path.exists("agents"):
    with open('agents') as agents: 
        print("[*] Found agents file")
        current_agents = pickle.load(agents) 
    agents.close
print("[*] Ctrl+C to stop")
try: 
	while True: 
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            r = requests.get(empire_url + "/api/agents?token=" + empire_apikey, verify=False)
            json_response = json.loads(r.content)
            agents = json_response["agents"] 

            for active_agent in agents:                    
                agent_id = active_agent.get("sessionID")    
                if agent_id not in current_agents: 
			print("[* ]New agent ({0}) Woohoo!".format(agent_id))
                        external_ip = active_agent.get("external_ip")
                        hostname = active_agent.get("hostname")
			os_details = active_agent.get("os_details")
			username = active_agent.get("username")

			current_agents.append(agent_id)

                        body = """
ID: {0}
IP: {1}
Host: {2}
OS: {3}
User: {4}
                        """.format(agent_id, external_ip, hostname, os_details, username)

                        for recipient in recipients: 
                            address = recipient[0] + "@" + recipient[1]
                            send_email(gmail_user, gmail_password, address, subject, body)
            time.sleep(2)
except KeyboardInterrupt:
    print "[*]Caught interrupt. Saving config"
    config_file = open("config", 'w')
    pickle.dump(recipients, config_file)
    config_file.close

    agents_file = open("agents", 'w')
    pickle.dump(current_agents, agents_file)
    agents_file.close
    pass

