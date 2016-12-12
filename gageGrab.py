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

#------------------------------------------------

# Listing of all station types :
stationTypeDict = {'AG' : 'Aggregate groundwater use', 'AS' : 'Aggregate surface-water-use',
                'AT' : 'Atmosphere', 'AW' : 'Aggregate water-use establishment',
                'ES' : 'Estuary', 'FA' : 'Facility', 'FA-AWL' : 'Animal waste lagoon',
                'FA-CI' : 'Cistern', 'FA-CS' : 'Combined Sewer', 'FA-DV' : 'Diversion',
                'FA-FON' : 'Field, Pasture, Orchard, or Nursery', 'FA-GC' : 'Golf Course',
                'FA-HP' : 'Hydroelectric Plant', 'FA-LF' : 'Landfill', 'FA-OF' : 'Outfall',
                'FA-PV' : 'Pavement', 'FA-QC' : 'Lab or Sample Prep Area', 'FA-SEW' : 'Wastewater Sewer',
                'FA-SPS' : 'Septic System', 'FA-STS' : 'Storm Sewer', 'FA-TEP' : 'Thermoelectric Plant',
                'FA-WDS' : 'Water Distribution System', 'FA-WIW' : 'Waste Injection Well',
                'FA-WTP' : 'Water-supply Treatment Plant', 'FA-WU' : 'Water Use Establishment',
                'FA-WWD' : 'Wastewater land application', 'FA-WWTP' : 'Wastewater Treatment Plant',
                'GL' : 'Glacier', 'GW' : 'Well', 'GW-CR' : 'Collector or Ranney type well',
                'GW-EX' : 'Extensometer Well', 'GW-HZ' : 'Hyporheic-zone Well',
                'GW-IW' : 'Interconnected Well', 'MW' : 'Multiple Wells', 'GW-TH' : 'Test Hole',
                'LA' : 'Land', 'LA-EX' : 'Excavation', 'LA-OU' : 'Outcrop', 'LA-PLY' : 'Playa',
                'LA-SH' : 'Soil Hole', 'LA-SNK' : 'Sinkhole', 'LA-SR' : 'Shore', 'LA-VOL' : 'Volcanic Vent',
                'LK' : 'Lake', 'OC' : 'Ocean', 'OC-CO' : 'Coastal', 'SB' : 'Subsurface', 'SB-CV' : 'Cave',
                'SB-GWD' : 'Groundwater Drain', 'SB-TSM' : 'Tunnel', 'SB-UZ' : 'Unsaturated Zone',
                'SP' : 'Spring', 'SS' : 'Specific Source', 'ST' : 'Stream', 'ST-CA' : 'Canal',
                'ST-DCH' : 'Ditch', 'ST-TS' : 'Tidal Stream', 'WE' : 'Wetland'}

# Command Line Arguments:
parser = argparse.ArgumentParser(description='USGS Station Data Grabber')
parser.add_argument('fipsCode',
                    help='County FIPS Codes. May be separated by commas. Ex: 37119,37118')
parser.add_argument('outFile',
                    help='File to save GEOJSON output to')
args=parser.parse_args()

# Grab data from URL...
response = urllib.request.urlopen("http://waterservices.usgs.gov/nwis/iv/?countyCd="+args.fipsCode)
tree = etree.parse(response)
root = tree.getroot()
#print(root[:][0][0].text)
# Prepare outfile
fileName = open(args.outFile,'w')

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

	# Station Information...
        if tempName != root[i][0][0].text: # Only provide station info if this is a new station...
            if i > 1 :
                stID=stID+1
                print('}',file=fileName)
                print( '},',file=fileName)
            print( '  { "type": "Feature",', end='',file=fileName)
            print( '"geometry": {"type": "Point", "coordinates": [',root[i][0][3][0][1].text,',' ,root[i][0][3][0][0].text,']},',file=fileName)
            print('"properties": {"stationName": "',root[i][0][0].text,'"', end='',file=fileName)
            print(',"stationType": "',root[i][0][4].text,'"', end='',file=fileName)
            print( ',"stID":"',stID,'"', end='',file=fileName)
            print( ',"usgsID":"',root[i][0][1].text,'"',end='',file=fileName)
            tempName = root[i][0][0].text

        # ID Report type and assign appropriate property...        
        if root[i][1][0].get("variableID") == '45807197' :
            print( ',"streamFlow":"',root[i][2][0].text,'"', end='',file=fileName)
        if root[i][1][0].get("variableID") == '45807202' :
            print( ',"gageHeight":"',root[i][2][0].text,'"', end='',file=fileName)
        if root[i][1][0].get("variableID") == '45807140' :
            print( ',"rainfall":"',root[i][2][0].text,'"', end='',file=fileName)

    i = i+1 # Advance loop counter

# Close all brackets
print('}',file=fileName)
print('}',file=fileName)
print(']',file=fileName)
print('}',file=fileName)
