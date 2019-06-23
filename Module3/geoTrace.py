from geoip import geolite2
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import itertools
import socket
import subprocess
import re
import sys

	#Check to see if an IP or hostname was entered and if not print usage information.
if len(sys.argv) < 2:
	print('Usage: python geoTrace [IP or Hostname]')
	print('Enter either the IP or Hostname of a website that you would like to visualize the path from you to it.')
	exit()

	#gethostbyname works if you give it the host name or IP
ip = socket.gethostbyname(sys.argv[1]) #Get the IP of the host provided
hop = 0 #Variable to keep up with the number of hops between current location and the destination
geolocator = Nominatim() #Create the geolocator used to getting the names of locations
trace = subprocess.Popen(['tracert','-w','10', ip], stdout=subprocess.PIPE) #Use the OS (Windows) traceroute function
route = trace.stdout.readline() #Start reading the input of the traceroute
	#Variables to keep up with the current hop IP, the previous location, save the coordinates, the location name, and hop number of each match
currentIP = ''
prevCityState = ''
lat=[]
long=[]
textPoint=[]
hopPlot=[]
	#As long as we still have more locations in our traceroute, we will go through each line of it
while route:
		#if we find an IP address in the current traceroute line, this regex pulls it out
	match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', route)
		#if we found an IP, then get the location of it if possible
	if match:
		currentIP = str(format(match.group()))
		geoloc = geolite2.lookup(currentIP)
			#If we did find a location then we can start pulling more information about it out.
		if(geoloc):
			loc = geolocator.reverse(geoloc.location, language='en')
			adrs = loc.raw['address']
			#print(adrs)
			try:
				cityState = adrs['city']+', '+adrs['state']
			except KeyError:
				cityState = adrs['state']+', '+adrs['country']
				#if we still have hop as 0, we haven't moved yet so this is where our destination is.
				#Setup our information here.
			if hop == 0:
				print('Geotracing route to ' + currentIP + ' in ' +cityState)
				print('hop number\tIP at hop\t\tIP Location')
				prevCityState = cityState
				#otherwise we can pull out the information we want to display and add the information we want to keep to our lists
			else:
				print(str(hop) + '\t\t' + currentIP +'\t\t'+cityState)
					#If we are bouncing around the same "city" for multiple hops, this cleans it up looks-wise so its only plotted once
				if prevCityState != cityState:
					xpt,ypt = geoloc.location
					lat.append(xpt)
					long.append(ypt)
					textPoint.append(str(hop)+': '+cityState)
					hopPlot.append('$'+str(hop)+'$') #formats the hop number to be used as a marker later
					prevCityState = cityState
				else:
					prevCityState = cityState
			#If we can't find a location for the current IP, it could be an internal location or unavailable so we don't keep this information
			#We do output it the same, just with the location not explicitly specified
		else:
			print(str(hop) + '\t\t' + currentIP +'\t\t'+'Unknown/Internal Location')
		hop+=1 #Increment hop
	route = trace.stdout.readline() #Read the next traceroute output line if it is there
	
	#Check to see if the traceroute completed.  If it didn't make it beyond the first hop
	#	or if it didn't reach the destination, then it isn't plotted on the map.
if hop == 1 or currentIP != ip:
	print('Unable to complete traceroute.')
	
	#If the traceroute completes, then plot it on a map.
	#First create the figure and then set up the map projection and size.
else:
	plt.figure(figsize=(8,8))
	map = Basemap(projection='lcc', resolution=None, width=8E6, height=8E6, lat_0=45, lon_0=-100,)
	map.etopo(scale=0.5, alpha=0.5)
	marker = itertools.cycle(hopPlot) #Location labels to use, for now the hop numbers
	map.plot(long,lat,marker='o', color='k', latlon=True) #Plot the list of points and the lines between them
	for x,y in zip(long, lat): #For each point, plot the lable at a slight offset
		map.plot(x,y+1.5,marker=marker.next(), color='k', latlon=True)
	plt.show() #show the figure
