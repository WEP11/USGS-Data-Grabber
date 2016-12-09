##################################################
#                                                #
#              USGS Data Grabber                 #
#         GeoReferenced Station Creator          #
#       Author: Warren Pettee (@wpettee)         #
#                     2016                       #
##################################################
import requests
import urllib
from urllib.request import urlopen
import xml.etree.ElementTree as etree
import geojson

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

stationName = []
stationLat = []
stationLon = []
stationType = []
gageHeight = []

response = urllib.request.urlopen("http://waterservices.usgs.gov/nwis/iv/?countyCd=37119")
tree = etree.parse(response)
root = tree.getroot()

fileName = open('usgsMeck.geojson','w')

i=0
tempName=' '

print( '{ "type": "FeatureCollection",',file=fileName)
print( '"features": [',file=fileName)   
for child in root:
    if i >= 1 :
        if tempName != root[i][0][0].text:
            if i > 1 :
                print('}',file=fileName)
                print( '},',file=fileName)
            print( '  { "type": "Feature",', end='',file=fileName)
            print( '"geometry": {"type": "Point", "coordinates": [',root[i][0][3][0][1].text,',' ,root[i][0][3][0][0].text,']},',file=fileName)
            print('"properties": {"stationName": "',root[i][0][0].text,'"', end='',file=fileName)
            print(',"stationType": "',root[i][0][4].text,'"', end='',file=fileName)
            
            tempName = root[i][0][0].text

            # stationType.append(root[i][0][4].text)
                
        if root[i][1][0].get("variableID") == '45807197' :
            print( ',"streamFlow":"',root[i][2][0].text,'"', end='',file=fileName)
            #print(stationName[i-1], ' Streamflow: ', root[i][2][0].text, ' ',root[i][2][0].get("dateTime"))
        if root[i][1][0].get("variableID") == '45807202' :
            print( ',"gageHeight":"',root[i][2][0].text,'"', end='',file=fileName)
            #print(stationName[i-1], ' Gageheight: ', root[i][2][0].text, ' ',root[i][2][0].get("dateTime"))
        if root[i][1][0].get("variableID") == '45807140' :
            print( ',"rainfall":"',root[i][2][0].text,'"', end='',file=fileName)
            #print(stationName[i-1], ' Rainfall: ', root[i][2][0].text, ' ',root[i][2][0].get("dateTime"))
    i = i+1
print('}',file=fileName)
print('}',file=fileName)
print(']',file=fileName)
print('}',file=fileName)
