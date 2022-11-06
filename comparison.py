#Compare CSV Files V1.0 (28/07/2020)
#Load required modules
import subprocess
from subprocess import PIPE
import pandas as pd
import re
import os
import time
import csv
import json

URL_list = []
found_dict = {}
reject_dict = {}
x = 0
i = 0

#Retrieve SID
stream = subprocess.run("curl -u admin:splunkhack -k https://localhost:8089/services/search/jobs -d search='search source=stream:* host=frost-virtual-machine'", shell=True, stdout=PIPE).stdout.decode()

alien = subprocess.run("curl -u admin:splunkhack -k https://localhost:8089/services/search/jobs -d search='search source=/home/frost/Desktop/alienVault.json index=alienvault host=frost-virtual-machine sourcetype=_json2'", shell=True, stdout=PIPE).stdout.decode()

stream_sid = re.findall("<sid>(\S+)<\/sid>", stream)
alien_sid = re.findall("<sid>(\S+)<\/sid>", alien)

time.sleep(5)

#Retrieve Results in CSV mode using SID
stream_csv = subprocess.run("curl -u admin:splunkhack -k https://localhost:8089/services/search/jobs/" + stream_sid[0] + "/results --get -d output_mode=csv > stream_Retrieve.csv", shell=True, stdout=PIPE).stdout.decode()

alien_csv = subprocess.run("curl -u admin:splunkhack -k https://localhost:8089/services/search/jobs/" + alien_sid[0] + "/results  --get -d output_mode=csv > alien_Retrieve.csv", shell=True, stdout=PIPE).stdout.decode()

#Using _raw section
F1 = (list(pd.read_csv('alien_Retrieve.csv')['_raw']))
F2 = (list(pd.read_csv('stream_Retrieve.csv')['_raw']))

F1_length = len(F1)
F2_length = len(F2)

if (F1_length > F2_length):
	Max = F1_length
	Min = F2_length
else:
	Max = F2_length
	Min = F1_length

for i in range(F1_length):
	regex = re.findall(r':\s"\S+', F1[i])
	regex_edit = regex[0].replace(': "', '').replace('",', '')
	URL_list.insert(i, regex_edit)

#print(type(URL_list[0]))
#print(type(F2[0]))

for i in range(Max):
	stream_data = F2[i]
	for x in range(len(URL_list)):
		if (stream_data.find(URL_list[x]) != int(-1)):
			found_dict['Indicator'] = URL_list[x]
			found_dict['Source'] = stream_data
			#print ("URL: " + URL_list[x] + "\nStream: " + stream_data + "\nStatus: True")
			#print()
		else:
			reject_dict[URL_list[x]] = stream_data
			#print("URL: " + URL_list[x] + "\nStream: " + stream_data + "\nStatus: False")
			#print()


if (os.path.isfile('home/frost/Desktop/alert.json') == True):
	os.remove('alert.json')

with open('alert.json', 'w') as output_file:
	json.dump(found_dict, output_file)

subprocess.run(['cd ~/Desktop', 'chmod 666 alert.json'], shell=True)


