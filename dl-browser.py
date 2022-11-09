#!/bin/python3

import requests
import urllib
import os
from requests.auth import HTTPBasicAuth

# global variables
rootFolder = "lacroi-m/"
baseUrl = "https://base_url.domain.extension/files/" + rootFolder
username = ""
password = ""

def createFolder(directoryName):
	try: 
		os.mkdir(directoryName) 
	except OSError as error: 
		print(error)

def downloadFile(url, fileName, directoryName):
	destination = directoryName+"/"+fileName
	if directoryName is "":
		destination = fileName
	if os.path.exists(destination):
		print(destination + " already exists, skipping...")
		return
	newUrl = url + fileName

	if directoryName != "" and os.path.exists(directoryName) == False:
		createFolder(directoryName)

	response = requests.get(newUrl, auth=HTTPBasicAuth(username, password))
	open(destination, "wb").write(response.content)

def GoToDirectory(url, directoryName):
	newUrl = url + urllib.parse.quote(directoryName) + "/"
	response = requests.get(newUrl, auth=HTTPBasicAuth(username, password))

	for element in response.json():
		if element["type"] == 'directory':
			GoToDirectory(newUrl, element["name"])
		if element["type"] == 'file':
			downloadFile(newUrl, element["name"], directoryName)

def start():
	response = requests.get(baseUrl, auth=HTTPBasicAuth(username, password))
	for element in response.json():
		if element["type"] == "directory":
			GoToDirectory(baseUrl, element["name"])
		if element["type"] == "file":
			downloadFile(baseUrl, element["name"], "")

start()