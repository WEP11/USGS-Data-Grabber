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
parser = argparse.ArgumentParser(description='USGS Station Data Grabber')
parser.add_argument('fipsCode',
                    help='County FIPS Codes. May be separated by commas. Ex: 37119,37118')
parser.add_argument('outFile',
                    help='File to save GEOJSON output to')
args=parser.parse_args()

county_list = args.fipsCode.split(',') # Generate a list of fips codes...

# Prepare outfile
fileName = open(args.outFile,'w')

# Get flood information...
colnames = ['nwsID','usgsID','action','minor','moderate','major','unit','name','state']
data = pandas.read_csv('gageInfo/floodStages.csv',skiprows=5, names=colnames)
floodID = data.usgsID.tolist()
floodAction = data.action.tolist()
floodMinor = data.minor.tolist()
floodModerate = data.moderate.tolist()
floodMajor = data.major.tolist()
floodUnit = data.unit.tolist()

# Begin printing GeoJSON Format...
print( '{ "type": "FeatureCollection",',file=fileName)
print( '"features": [',file=fileName)  
 
# Prepare to enter main loop...
i=0 # Counter
stID=0 # Station ID Counter
tempName=' ' # Station name tracking
stage = 0
prevVar = 0  

for countyCode in county_list: # Request by county. This lets you do giant lists
    # Grab data from URL...
    response = urllib.request.urlopen("http://waterservices.usgs.gov/nwis/iv/?countyCd="+countyCode)

    tree = etree.parse(response)
    root = tree.getroot()

    lineCount = 0

    # Loop through all station reports...
    for child in root:
        if lineCount > 0 : # First entry is a request summary, so skip that
            # Yup, Variables...
            # Parameter is arbitrary, different XML call per variable per station
            # that's why we have to figure out what reading it is in the IF statements
            # below...
            stationName = root[lineCount][0][0].text
            usgsID = root[lineCount][0][1].text
            stationType = root[lineCount][0][4].text
            lat = root[lineCount][0][3][0][0].text
            lon = root[lineCount][0][3][0][1].text
            parameter = root[lineCount][2][0].text 
            parameterID = root[lineCount][1][0].get("variableID")
	    # Station Information...
            if tempName != stationName: # Only provide station info if this is a new station...
                if i > 1 : # If this isn't our first station, wrap up our last one
                    stID=stID+1
                    if stage > 0:
                        print( ',"icon":"' + floodIcons[stage] + '"', end='',file=fileName)
                    elif stage == 0 and lastStationType == 'ST':
                        print( ',"icon":"' + floodIcons[0] + '"', end='',file=fileName)
                    elif stage == 0 and lastStationType == 'AT':
                        print( ',"icon":"green_water-15"', end='',file=fileName)
                    print('}',file=fileName)
                    print( '},',file=fileName)     
                    prevVar = 0           

                j=0
                for site in floodID: # Firstly, can this station give us flood info?
                    if str(site).strip(' \t\n\r') == str(usgsID).strip(' \t\n\r') :
                        floodOption = 1
                        if floodUnit[j] == 'ft' and parameterID == '45807202' and prevVar == 0 and parameter is not None :
                            stage = usgs.floodStage(float(parameter),j,floodAction,floodMinor,floodModerate,floodMajor)
                            prevVar = 1
                        elif floodUnit[j] == 'cfs' and parameterID == '45807197' and prevVar == 0 and parameter is not None :
                            stage = usgs.floodStage(float(parameter),j,floodAction,floodMinor,floodModerate,floodMajor)
                            prevVar = 1
                        else:
                            stage = 0
                    else:
                        floodOption = 0
                    j=j+1
                        
                print( '  { "type": "Feature",', end='',file=fileName)
                print( '"geometry": {"type": "Point", "coordinates": [' + lon + ',' + lat + ']},' ,file=fileName)
                print('"properties": {"stationName": "' + stationName + '"' , end='' ,file=fileName)
                print(',"stationType": "' + stationType + '"' , end='',file=fileName)
                print( ',"stID":"' + str(stID) + '"' , end='',file=fileName)
                print( ',"usgsID":"'+ str(usgsID) + '"' ,end='',file=fileName)
                tempName = stationName

            # ID Report type and assign appropriate property...        
            if parameterID == '45807197' :
                print( ',"streamFlow":"' + str(parameter) + '"', end='',file=fileName)
            if parameterID == '45807202' :
                print( ',"gageHeight":"' + str(parameter) + '"', end='',file=fileName)
            if parameterID == '45807140' :
                print( ',"rainfall":"' + str(parameter) + '"', end='',file=fileName)

            lastStationType = stationType
            lastStId = usgsID
            i = i+1 # Advance loop counter
        lineCount = lineCount+1

# Close last feature
print('}',file=fileName)
print('}',file=fileName)

# Close feature collection
print(']',file=fileName)
print('}',file=fileName)
