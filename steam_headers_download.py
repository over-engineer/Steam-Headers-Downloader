#!/usr/bin/env python

# ################################################################################
# 
# Steam Headers Downloader
# A script to download Steam header images
# 
# v0.1: 2015-04-29
# 
# ################################################################################
# 
# The MIT License (MIT)
# 
# Copyright (c) 2015 Dinos
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
# ################################################################################

import xml.etree.ElementTree as ET
import sys, os
import urllib

def asciiTitle():
	print "   _____ __                          _______ __         \n  / ___// /____  ____ _____ ___     /_  __(_) /__  _____\n  \__ \/ __/ _ \/ __ `/ __ `__ \     / / / / / _ \/ ___/\n ___/ / /_/  __/ /_/ / / / / / /    / / / / /  __(__  ) \n/____/\__/\___/\__,_/_/ /_/ /_/    /_/ /_/_/\___/____/ \n"

def getValidFilename(name):
	validChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-+!.,'_()[] "
	filename = name + ".jpg"
	
	return "".join(c for c in filename if c in validChars)
	
def getSteamXML(username):
	xmlUrl = "http://steamcommunity.com/id/" + username + "/games?tab=all&xml=1"
	return urllib.urlopen(xmlUrl)

def getImages(username, statusOutputEnabled, pathToSave):
	tree = ET.parse(getSteamXML(username))
	root = tree.getroot()
	
	if (root.find("error") != None):
		print root.find("error").text
		sys.exit(0)
	
	for game in root.iter("game"):
		name = game.find("name").text
		appID = game.find("appID").text
		
		imgUrl = "http://cdn.akamai.steamstatic.com/steam/apps/" + appID + "/header.jpg"
		
		if (urllib.urlopen(imgUrl).getcode() == 200):		
			if (statusOutputEnabled == "Y"):
				print "Downloading \"" + name + "\" image..."
			
			urllib.urlretrieve(imgUrl, pathToSave + "/" + getValidFilename(name))
		
	print "Download complete"

def main():
	asciiTitle()
	
	username = raw_input("Steam username: ")
	
	statusOutputEnabled = ""
	while (statusOutputEnabled != "Y" and statusOutputEnabled != "N"):
		statusOutputEnabled = raw_input("Status output (y/n): ").upper()
		if (statusOutputEnabled != "Y" and statusOutputEnabled != "N"):
			print "Invalid input"
			
	pathToSave = raw_input("Path to save (leave blank for current directory): ")
	if (pathToSave == ""):
		pathToSave = "."
	else:
		pathToSave = pathToSave.replace("\\", "/")
		if (pathToSave[-1:] == "/"):
			pathToSave = pathToSave[:-1]
	if (os.path.isdir(pathToSave) == False):
		print "Directory does not exist"
		sys.exit(0)
	
	getImages(username, statusOutputEnabled, pathToSave)

if __name__ == "__main__":
	main()
