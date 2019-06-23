# Module 3 - geoTrace

Allows for the geolocation along a traceroute so that you can see the rough path that your traffic is taking in a more recongnizable format.
The path will also be plotted on a map with each unique hop labled.

## Requirements:

- Windows OS
- Python 2.7
- Extra Modules: geoip, matplotlib, basemap, geopy

## Usage:

```bash
python geoTrace.py [IP address or Hostname]
```
- Either the IP address or the hostname of the target location may be used.

## Current Limitations:

- Works using Window's tracert function, so it is Windows specific.
- Visual representation is for North America only currently.
- Some locations are not able to be displayed properly.

## Future Work:

- Correct the location tracking for some edge cases.
- Adjust how the map is generated so that other regions or world-wide addresses may be shown on the map.
- Improve the representation of the points on the map beyond hop number.