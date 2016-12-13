# USGS-Data-Grabber
This simply grabs all USGS sites in a list of counties and returns the instantaneous values as a geojson file. Check out the example at http://weather.uncc.edu/beta .

The program will take a list of any size containing county FIP codes and split it up into individual calls. A single feature is created for each station containing the individual parameters. If the station ID is recognized on the NWS flood stage list, then a colored icon will be assigned to match the flood stage.

Flood stage icons can be changed in the array at the top of the script, and the stage-icon associations can be changed by changing the return values inside the `floodstage()` (within usgs.py) function to match the corresponding icon array index.

**Usage:** `python gageGrab.py <County FIP Codes> <geoJSON output file>`

*County Fip Codes:* This is a list of 5 digit county FIP codes, separated by commas for multiple

*geoJSON Output File:* This is the file to be output

*Example:* `python gageGrab.py 37119,37179 output.geojson`

** Additional Information:**

usgs.py contains useful functions and dictionaries when dealing with USGS station data. The gageInfo folder simply contains the NWS Listing that associates the NWS AHPS station ID to the USGS station ID as well as the corresponding flood stage thresholds. There is also a script which creates that listing by ripping the USGS ID corresponding to the NWS ID from the AHPS RSS feed, it then takes the flood thresholds from an AHPS shapefile attribute table that I've exported for use with the Python program.
