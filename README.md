# USGS-Data-Grabber
This simply grabs all USGS sites in a list of counties (for now just Mecklenburg Co NC) and returns the instantaneous values as a geojson file. Check out the example at http://weather.uncc.edu/beta

**Usage:** `python gageGrab.py <County FIP Codes> <geoJSON output file>`
 *County Fip Codes:* This is a list of 5 digit county FIP codes, separated by commas for multiple
 *geoJSON Output File:* This is the file to be output

*Example:* `python gageGrab.py 37119,37179 output.geojson`


In the future this will:

1. Allow user input of site location
2. Export 7-Day Charts for each site
3. Export additional datatypes (perhaps netcdf?)
