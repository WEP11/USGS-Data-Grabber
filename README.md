# USGS-Data-Grabber
Tired of the USGS running on servers from the dawn of time? This makes grabbing and georeferencing USGS data easier and faster than waiting on them to modernize (remember, they're on geological timescales).

The plan is a package that allows you to:

1. Provide a station description tsv from the USGS site of all of the sites you're interested in
2. Turn that list into a georeferenced file
3. Gain the ability to regularly run an updater program which will grab data for each station and will be capable of providing plots or raw data in csv format.

This is not intended to download long-term datasets. We must respect the fact that they are running on old Gateway 2000's and thus meet their request of no more than 10,000 data entry requests.
