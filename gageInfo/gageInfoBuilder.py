####################################################
#                                                  #
#         USGS vs NWS List Maker                   #
#                                                  #
#       Author: Warren Pettee                      #
#       Github WEP11 Twitter: @wpettee)            #
# Usage: python gageGrab.py 37119 usgsMeck.geojson #
####################################################

import argparse
import requests
import urllib
from urllib.request import urlopen
import xml.etree.ElementTree as etree
import pandas

stateList = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "GU","dc"]

fileName = open("floodStages.csv",'w')

colnames = ['ahpsID', 'name', 'latitude', 'longitude', 'waterbody','state','action','flood','moderate','major','lt','units']
data = pandas.read_csv('nwsData.csv', names=colnames)

ahpsID = data.ahpsID.tolist()
action = data.action.tolist()
flood = data.flood.tolist()
moderate = data.moderate.tolist()
major = data.major.tolist()
units = data.units.tolist()
name = data.name.tolist()
stnState =  data.state.tolist()



print( 'USGS ID, NWS ID, Station Name, Action, Minor, Moderate, Major',file=fileName)
for state in stateList:
    response = urllib.request.urlopen("http://water.weather.gov/ahps2/rss/obs/"+state.lower()+".rss")
    tree = etree.parse(response)
    root = tree.getroot()
    for j in range(9,len(root[0])):
        i=0
        for stn in ahpsID :
            if stn in root[0][j][0].text:
                if "USGS ID" in root[0][j][2].text:
                    description = root[0][j][2].text
                    dSplit = description.split("USGS ID:")[1]
                    usgsID= dSplit.split("</a>")[0]
                    print(stn,usgsID,action[i],flood[i],moderate[i],major[i],units[i],name[i],stnState[i],sep=',',file=fileName)
            i=i+1
            
