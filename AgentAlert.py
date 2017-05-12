import json
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import smtplib


# CHANGEME
apikey=""
sms_gateway=""
sms_number=""
url="https://localhost:1337/api/agents?token="
gmail_user=""
gmail_password=""
# END OF CHANGEME
recipient=sms_number + "@" + sms_gateway
subject="EMPIRE AGENT"
body="test"

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
		print 'successfully sent the mail'
	except:
		print "failed to send mail"

current_agents = []

while True: 
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	r = requests.get(url+apikey, verify=False)
	json_response = json.loads(r.content)
	agents = json_response["agents"]

	for active_agent in agents: 
		agent_id = active_agent.get("sessionID")
		if agent_id not in current_agents: 
			print("New shell! Woohoo!")
			current_agents.append(agent_id)
			send_email(gmail_user, gmail_password, recipient, subject, body)
	print("Sleeping")
	time.sleep(5)




