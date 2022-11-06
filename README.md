# Project_FYP
As part of my graduation requirements, I was required to do a Final Year Project(FYP). My team(consisting of 3 people) were required create a Real-Time Malware Threat
Analysis System. The project was split into three parts with me being in-charge of Malware Threat Feed and Classification. My part of the project was to:
+ "pull" indicators of compromises (IOC) feeds from threat intelligence sites for malwares.
+ Using Splunk to analyse network traffic for phishing emails/websites.
+ Correlate and classify the traffic.
+ Create an interactive dashboard to visualize the correlation with GeoMap.

The repository contains two different files. The file named "alienVault.py" is used to pull IOCs from an open threat exchange website "AlienVault". The second file,
"comparison.py" is used to compare the network file (which contains the phishing site) and IOC feeds from the threat intelligence sites. If a match is found in both files
a file name "alert.json" would be created. 


# What Have I Learnt?
+ Using various python modules (requests, json, csv, socket, ssl) to pull IOCs from AlienVault Open Threat Exchange.
+ Integrating both files (alienVault.py, comparison.py) with Splunk.
+ Displaying key information on Splunk Dashboard via use of Graphs, Charts & GeoMap.
