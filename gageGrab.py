####################################################
#                                                  #
#              USGS Data Grabber                   #
#         GeoReferenced Station Creator            #
#       Author: Warren Pettee (@wpettee)           #
#                                                  #
# Usage: python gageGrab.py 37119 usgsMeck.geojson #
####################################################

import argparse
import requests
import urllib
from urllib.request import urlopen
import xml.etree.ElementTree as etree
import pandas
import usgs
#------------------------------------------------
floodIcons = ['school-15','green_school-15','yellow_school-15','red_school-15']
# Command Line Arguments:
#parser = argparse.ArgumentParser(description='USGS Station Data Grabber')
#parser.add_argument('fipsCode',
#                    help='County FIPS Codes. May be separated by commas. Ex: 37119,37118')
#parser.add_argument('outFile',
#                    help='File to save GEOJSON output to')
#args=parser.parse_args()

# Get flood information...
colnames = ['nwsID','usgsID','action','minor','moderate','major','unit','name','state']
data = pandas.read_csv('gageInfo/floodStages.csv',skiprows=5, names=colnames)
floodID = data.usgsID.tolist()
floodAction = data.action.tolist()
floodMinor = data.minor.tolist()
floodModerate = data.moderate.tolist()
floodMajor = data.major.tolist()
floodUnit = data.unit.tolist()

# Grab data from URL...
#response = urllib.request.urlopen("http://waterservices.usgs.gov/nwis/iv/?countyCd="+args.fipsCode)
response = urllib.request.urlopen("http://waterservices.usgs.gov/nwis/iv/?countyCd=37119")
tree = etree.parse(response)
root = tree.getroot()
#print(root[:][0][0].text)
# Prepare outfile
#fileName = open(args.outFile,'w')
fileName = open('test.geojson','w')
# Prepare to enter main loop...
i=0 # Counter
stID=0 # Station ID Counter
tempName=' ' # Station name tracking

# Begin printing GeoJSON Format...
print( '{ "type": "FeatureCollection",',file=fileName)
print( '"features": [',file=fileName)   

# Loop through all station reports...
for child in root:
    if i >= 1 : # First entry is a request summary, so skip that
        # Yup, Variables...
        # Parameter is arbitrary, different XML call per variable per station
        # that's why we have to figure out what reading it is in the IF statements
        # below...
        stationName = root[i][0][0].text
        usgsID = root[i][0][1].text
        stationType = root[i][0][4].text
        lat = root[i][0][3][0][0].text
        lon = root[i][0][3][0][1].text
        parameter = root[i][2][0].text 
        
	# Station Information...
        if tempName != stationName: # Only provide station info if this is a new station...
            j=0
            floodOption = 0
            for site in floodID: # Firstly, can this station give us flood info?
                if str(site).strip() == usgsID:
                    floodOption = 1
                    if floodUnit[j] == 'ft':
                        floodOptHgt = 1
                        floodPlace = j
                    elif floodUnit[j] == 'cfs':
                        floodOptFlo = 1
                        floodPlace = j
                    else:
                        floodOption = 0
                else:
                    floodOption = 0
                j=j+1
                    
            if i > 1 :
                stID=stID+1
                print('}',file=fileName)
                print( '},',file=fileName)
            print( '  { "type": "Feature",', end='',file=fileName)
            print( '"geometry": {"type": "Point", "coordinates": [',lon,',' ,lat,']},',file=fileName)
            print('"properties": {"stationName": "',stationName,'"', end='',file=fileName)
            print(',"stationType": "',stationType,'"', end='',file=fileName)
            print( ',"stID":"',stID,'"', end='',file=fileName)
            print( ',"usgsID":"',usgsID,'"',end='',file=fileName)
            tempName = stationName

        # ID Report type and assign appropriate property...        
        if root[i][1][0].get("variableID") == '45807197' :
            print( ',"streamFlow":"',parameter,'"', end='',file=fileName)
            if floodOption == 1 and floodOptHgt == 1 :
                stage = usgs.floodStage(parameter,floodPlace,floodAction,floodMinor,floodModerate,floodMajor)
                print( ',"icon":"',floodIcons[stage],'"', end='',file=fileName)
            else:
                print( ',"icon":"',floodIcons[0],'"', end='',file=fileName)
        if root[i][1][0].get("variableID") == '45807202' :
            print( ',"gageHeight":"',parameter,'"', end='',file=fileName)
            if floodOption == 1 and floodOptHgt == 1 :
                stage = usgs.floodStage(parameter,floodPlace,floodAction,floodMinor,floodModerate,floodMajor)
                print( ',"icon":"',floodIcons[stage],'"', end='',file=fileName)
            else:
                print( ',"icon":"',floodIcons[0],'"', end='',file=fileName)
        if root[i][1][0].get("variableID") == '45807140' :
            print( ',"rainfall":"',parameter,'"', end='',file=fileName)
            print( ',"icon":"green_water-15"', end='',file=fileName)

    i = i+1 # Advance loop counter

# Close all brackets
print('}',file=fileName)
print('}',file=fileName)
print(']',file=fileName)
print('}',file=fileName)
