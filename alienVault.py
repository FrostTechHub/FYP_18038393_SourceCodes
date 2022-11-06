#Splunk Script V1.0 (10/05/2020)
#Load required modules
import requests as requests
import json
import csv
import socket
import ssl
import subprocess
import os
import time

#Set Socket default timeout to 35 Secs
socket.setdefaulttimeout(35)

#Program makes an API call to Alienvault
def alienVault_api_call(requestURL, parameters, otx_KEY):
    headers = {'X-OTX-API-KEY' : otx_KEY["api_key"]}
    response = requests.get(url=requestURL, headers=headers, params=parameters )
    if response.status_code != 200:
        print(response.json())
        exit()
    data = response.json()
    return json.dumps(data['results'])

#Sub-function of main(), provides additional information 
def getInput(api_keys, limits):
    parameters = {"limit" : limits, "api_key" : api_keys}
    otx_KEY = {"api_key" : api_keys}
    requestURL = "https://otx.alienvault.com:443/api/v1/indicators/export?"
    
    #Calls the alienVault server to retrieve results based on fields
    return alienVault_api_call(requestURL, parameters, otx_KEY)

def main():
    #Mandatory Fields to retrieve results
    api_keys = "5fd123fff7069d7621e306877ab336b59048ce9ceab5234fe81a572da4d88ebc"
    limits = "100"
    
    incoming_input = getInput(api_keys, limits) #Call the function getInput to provide additional requirements
    data = json.dumps(incoming_input) #Converts incoming_input into json string
    data_loaded = json.loads(data) #Parse data variable and convert it into python dictionary
    res = json.loads(data_loaded) #Parse the python dictionary again..

    #Writes the value of the res variable into a file named alienVault.json
    with open('alienVault.json', 'w') as outfile:
        for i in range(len(res)):
            if (res[i]['type'] == "URL" or res[i]['type'] == "domain" or res[i]['type'] == "hostname" or res[i]['type'] == "IPv4"):
                json.dump(res[i], outfile)
    subprocess.run(['cd ~/Desktop', 'chmod 666 alienVault.json'], shell=True) #Grants read and write permission to all
    
if __name__ == "__main__":
    if (os.path.isfile('home/frost/Desktop/alienVault.json') == True):
        os.remove('alienVault.json')
        main()
    else:
        main()
else:
    print("Error - Conditional Statement Failed To Evaluate To True...")
    time.sleep(2)
    print("Exiting Program..")
    exit()