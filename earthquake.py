# -*- coding: utf-8 -*-
# Author: Zhiwei Xu
# Update date: 2017-08-30
# License: The MIT License

import datetime
import json
import ssl
import time
import urllib.request, urllib.error
import os

# Ignore SSL error
ssl._create_default_https_context = ssl._create_unverified_context

def main(type, save):

    # Get feed
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}.geojson'.format(type)
    print('\nFetching: {}'.format(url))
    try:
        raw = urllib.request.urlopen(url)
    except:
        print('\nNetwork Error!\n')
        return
    data = raw.read().decode()
    try:
        feed = json.loads(data)
    except:
        print('\nError: The parameter is invalid!\n')
        return None

    # Time
    update_time = feed['metadata']['generated'] / 1000.0
    new_update_time = datetime.datetime.fromtimestamp(update_time).strftime('%Y-%m-%d %H:%M:%S')
    print('\n* System local time: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('* Feed updated time: {}'.format(new_update_time))
    time.sleep(2)

    # Save prettified json
    if save == "yes":
        text_file = open("{}.json".format(type), "w")
        text_file.write(json.dumps(feed, indent=4))
        text_file.close()
        print('\nJSON file saved to {}'.format(os.getcwd()))
        time.sleep(2)
    else:
        pass

    # Print events info
    if len(feed['features']) == 0:
        print('\nNo earthquakes.\n')
        return None

    for event in feed['features']:

        # Beginning
        print('\n>>>>>\n')

        # Set Alias
        properties = event['properties']
        geometry = event['geometry']

        # Alert
        alert = properties['alert']
        if alert == 'yellow' or alert == 'orange' or alert == 'red':
            print('!!! ALERT: {} !!!'.format(alert.upper()))

        # Title
        mag = properties['mag']
        loc = properties['place']
        print('*** Location: {} / Magnitude: {} ***'.format(loc, mag))

        # Time
        event_time = properties['time'] / 1000.0
        new_event_time = datetime.datetime.fromtimestamp(event_time).strftime('%Y-%m-%d %H:%M:%S.%f')
        print('* Time: {}'.format(new_event_time[:-4]))

        # Type
        typ = geometry['type']
        print('* Type: {}'.format(typ))

        # Coordinates
        coord = geometry['coordinates']
        long = coord[0]
        lat = coord[1]
        dep = coord[2]
        if long > 0:
            longd = 'E'
        elif long < 0:
            longd = 'W'
        else:
            longd = ''
        if lat > 0:
            latd = 'N'
        elif lat < 0:
            latd = 'S'
        else:
            latd = ''
        long = abs(long)
        lat = abs(lat)
        print('* Coordinates:\n' +
              '    - Latitude:  {} {}\n'.format(lat, latd) +
              '    - Longitude: {} {}\n'.format(long, longd) +
              '    - Depth:     {} km'.format(dep))

        # Felt
        felt = properties['felt']
        if felt is None:
            print('* Felt reported: No Report')
        elif felt == 1:
            print('* Felt reported: 1 time')
        else:
            print('* Felt reported: {} times'.format(felt))

if __name__ == '__main__':
    print(
    "   ___          _   _                   _\n" \
    "  | __|__ _ _ _| |_| |_  __ _ _  _ __ _| |_____\n" \
    "  | _|/ _` | '_|  _| ' \/ _` | || / _` | / / -_)\n" \
    "  |___\__,_|_|  \__|_||_\__, |\_,_\__,_|_\_\___|\n" \
    "                           |_|\n" \
    "   _   _          _      _\n" \
    "  | | | |_ __  __| |__ _| |_ ___\n" \
    "  | |_| | '_ \/ _` / _` |  _/ -_)\n" \
    "   \___/| .__/\__,_\__,_|\__\___|\n" \
    "        |_|\n" \
    "\n*** Get Latest Earthquakes Update from USGS ***\n\n\n"\
    "Earthquakes Types\n\n"\
    "  * Magnitude\n"\
    "  significant - Significant\n"\
    "  4.5 - M4.5+\n"\
    "  2.5 - M2.5+\n"\
    "  1.0 - M1.0+\n"\
    "  all - All\n\n"\
    "  * Time range\n"\
    "  hour  - Past Hour\n"\
    "  day   - Past Day\n"\
    "  week  - Past Week\n"\
    "  month - Past Month\n"\
    "\n  e.g. 4.5_day -> M4.5+ earthquakes in the past day\n"\
    "       significant_week -> significant earthquakes in the past week\n\n"\
    )
    magnitude = str(input("Enter magnitude (default: 4.5): ")) or "4.5"
    time_range = input("Enter time range (default: day): ") or "day"
    save = str(input("Save original JSON [yes or no] (default: no): ")) or "no"
    type = magnitude + "_" + time_range
    main(type, save)
