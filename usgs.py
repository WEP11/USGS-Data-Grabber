#########################################
# USGS Library
#----------------------------------------
# Just useful lists and dictionaries
# when dealing with USGS Data
# Author: Warren Pettee
#########################################

# Dictionary of all station type identifiers:
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

# USGS Variable ID's to Human :
variables = {'45807197' : 'streamFlow', '45807202' : 'gageHeight', '45807140' : 'rainFall'}

# USGS Parameter Codes : (This is a VERY small portion of them)
variableCodes = {'00004' : 'streamWidth','00011':'waterTempF','00021':'airTempF','00025':'presInHg',
                '00032' : 'cloudCover','00035':'windSpdMph','00036':'windDir','00045':'rainFallIn',
                '00052' : 'humidity','00055':'streamVeloFps','00060':'discharge','00062':'resevoirElev',
                '00064' : 'streamDepth','00065':'gageHeight','00067':'tideStage','81027':'soilTemp'}

def floodStage(current,x,action,minor,mod,major) :
    if(current < action[x]):
        return 1
    elif(current > action[x] and current < minor[x]):
        return 2
    elif(current > minor[x] and current < mod[x]):
        return 3
    elif(current > mod[x] and current < major[x]):
        return 3
    elif(current > major[x]):
        return 3
    else:
        return 0
