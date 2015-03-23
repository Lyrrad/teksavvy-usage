#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import requests
import json
from dateutil.parser import parse
import datetime
import argparse
import sys
 

parser = argparse.ArgumentParser(description='Check TekSavvy Usage.')
parser.add_argument('-a', '--apikey', help='TekSavvy API Key')
parser.add_argument('-s', '--save', action='store_true')
args = parser.parse_args();

apikey = args.apikey;
if apikey is not None and args.save is True:
	config = {'apikey': apikey}
	with open('teksavvyUsageSettings.json', 'w') as f:
		json.dump(config, f)

if apikey is None:
	try:
		with open('teksavvyUsageSettings.json', 'r') as f:
			config = json.load(f)
			apikey = config['apikey']
	except IOError:
		pass
		

if apikey is None:
	print "API Key not found.  Please supply an API Key."
	parser.print_help()
	sys.exit(0)

url = 'https://api.teksavvy.com/web/Usage/UsageRecords'
r = requests.get(url, headers ={'TekSavvy-APIKey': apikey})
 
data = json.loads(r.text)
values = data['value']

while 'odata.nextLink' in data:
	url = data['odata.nextLink']
	r = requests.get(url, headers ={'TekSavvy-APIKey': apikey})
	data = json.loads(r.text)
	values.extend(data['value'])

curMonth = 0
curDay = 0;
firstDay = 0;
curOnPeakDownload = 0
curOnPeakUpload = 0
curOffPeakDownload = 0
curOffPeakUpload = 0
for element in values:
	date = parse(element['Date'])
	if curMonth != date.month:
		if curMonth != 0:
			print "Usage from "+str(datetime.date(1900, curMonth, 1).strftime('%B')) + " " + str(firstDay) + " to " + str(curDay)
			print "On Peak Download: " + str(curOnPeakDownload) + " GB"
			print "On Peak Upload: " + str(curOnPeakUpload) + " GB"
			print "Off Peak Download: " + str(curOffPeakDownload) + " GB"
			print "Off Peak Upload: " + str(curOffPeakUpload) + " GB"
		curOnPeakDownload = 0
		curOnPeakUpload = 0
		curOffPeakDownload = 0
		curOffPeakUpload = 0
		firstDay = date.day
	curOnPeakDownload += element['OnPeakDownload']
	curOnPeakUpload += element['OnPeakUpload']
	curOffPeakDownload += element['OffPeakDownload']
	curOffPeakUpload += element['OffPeakUpload']
	curMonth = date.month
	curDay = date.day

print "Usage from "+str(datetime.date(1900, curMonth, 1).strftime('%B')) + " " + str(firstDay) + " to " + str(curDay)
print "On Peak Download: " + str(curOnPeakDownload) + " GB"
print "On Peak Upload: " + str(curOnPeakUpload) + " GB"
print "Off Peak Download: " + str(curOffPeakDownload) + " GB"
print "Off Peak Upload: " + str(curOffPeakUpload) + " GB"
