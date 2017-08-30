# -*- coding: utf-8 -*-
# Author: Andy Xu
# Update date: 2017-08-26
# License: The MIT License

import datetime
import json
import ssl
import time
import urllib.request, urllib.error
import os
from importlib import util
if util.find_spec("click") is None:
    os.system("pip3 install click")
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# Ignore SSL error
ssl._create_default_https_context = ssl._create_unverified_context

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--type', '-t', prompt='Enter the feed type', help='Feed type. {Magnitude}_{Time}')
@click.option('--save/--no-save', '-s/-ns', default=False, help='Save original JSON file. (default: no)')
def main(type, save):
    '''

    $ python3 earthquake.py --type <arg> (--save)

    \b
      <arg>: {Magnitude}_{Time}

    \b
      * Magnitude
      significant - Significant
      4.5 - M4.5+
      2.5 - M2.5+
      1.0 - M1.0+
      all - All

    \b
      * Time
      hour  - Past Hour
      day   - Past Day
      week  - Past Week
      month - Past Month

    \b
      e.g. 4.5_day -> M4.5+ earthquakes in the past day
           significant_week -> significant earthquakes in the past week
    '''

    # Get feed
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}.geojson'.format(type)
    click.echo('\nFetching: {}'.format(url))
    try:
        raw = urllib.request.urlopen(url)
    except:
        print('\nNetwork Error!\n')
        return
    data = raw.read().decode()
    try:
        feed = json.loads(data)
    except:
        print('\nError: The parameter for --type is invalid!\n')
        return None

    # Time
    update_time = feed['metadata']['generated'] / 1000.0
    new_update_time = datetime.datetime.fromtimestamp(update_time).strftime('%Y-%m-%d %H:%M:%S')
    click.echo('\n* System local time: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    click.echo('* Feed updated time: {}'.format(new_update_time))
    time.sleep(2)

    # Print prettified json
    if save is True:
        text_file = open("{}.json".format(type), "w")
        text_file.write(json.dumps(feed, indent=2))
        text_file.close()
        click.echo('\nJSON file saved to {}'.format(os.getcwd()))
        time.sleep(2)
    else:
        pass

    # Print events info
    if len(feed['features']) == 0:
        click.echo('\nNo earthquakes.\n')
        return None

    for event in feed['features']:

        # Beginning
        click.echo('\n>>>>>\n')

        # Set Alias
        properties = event['properties']
        geometry = event['geometry']

        # Alert
        alert = properties['alert']
        if alert == 'yellow' or alert == 'orange' or alert == 'red':
            click.echo('!!! ALERT: {} !!!'.format(alert.upper()))

        # Title
        mag = properties['mag']
        loc = properties['place']
        click.echo('*** Location: {} / Magnitude: {} ***'.format(loc, mag))

        # Time
        event_time = properties['time'] / 1000.0
        new_event_time = datetime.datetime.fromtimestamp(event_time).strftime('%Y-%m-%d %H:%M:%S.%f')
        click.echo('* Time: {}'.format(new_event_time[:-4]))

        # Type
        typ = geometry['type']
        click.echo('* Type: {}'.format(typ))

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
        click.echo('* Coordinates:\n' +
              '    - Latitude:  {} {}\n'.format(lat, latd) +
              '    - Longitude: {} {}\n'.format(long, longd) +
              '    - Depth:     {} km'.format(dep))

        # Felt
        felt = properties['felt']
        if felt is None:
            click.echo('* Felt reported: No Report')
        elif felt == 1:
            click.echo('* Felt reported: 1 time')
        else:
            click.echo('* Felt reported: {} times'.format(felt))

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
    "\n*** Get Latest Earthquakes Update from USGS ***\n"
    )
    main()
