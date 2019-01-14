#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calendar
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET
import codecs, argparse, os, sys, urlparse, json, xmltv

# meta
script_ver = 0.2
script_dec = "Extracts informations from XMLTV data"

# cmd
cmd_get_content = "get_content"

# initialize arguments
parser = argparse.ArgumentParser(description=script_dec, version=str(script_ver))
parser.add_argument("-t", "--target", dest="target", action="store", help="target XMLTV file",
                    required=True)
parser.add_argument("-c", "--command", dest="command", action="store",
                    choices=[cmd_get_content],
                    help="command to execute for XMLTV file", required=True)

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout) # Force script to output UTF-8

# Parse UTC to localtime
def utc_to_local(utc_dt):
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%dT%H:%M')

def aslocaltimestr2(utc_dt):
    return utc_to_local(utc_dt).strftime('%H:%M')    


# execute stuff with given attributes
args = parser.parse_args()

# Handle error if target-file wasn´t found / isn´t readable
try:
    fh = open(args.target, 'r')
except IOError:
    print "\033[1;31;40mUnable to read target-file: \033[0;37;40m" + args.target
    sys.exit(1)

title = "none; "
subtitle = "; "
starttime = "2010-10-10T10:10; "
stoptime = "2010-10-10T10:10; "
showimage = "https://chanlogos.digitalterrorist.de/123tv.png; "
country = "none"
date = ""
category = ""


# Consolidate all data in a readable way
if args.command == cmd_get_content:
    tree = ET.parse(args.target)
    root = tree.getroot()
    # channel-name
    for child in root.iter('display-name'):
        channel = child.text + "; "
        if channel is None:
            channel = "none; "
    # channel-logo-url
    for child in root.iter('channel'):
        for src in child.iter('icon'):
            channelUrl = src.attrib['src'] + "; "
            if channelUrl is None:
                channelUrl = "http://chanlogos.xmltv.se/13thstreet.de.png; "     
    for child in root.iter('programme'): 
        # show-title
        for src in child.iter('title'):
            title = src.text + "; "
            if title is None:
                title = "none; "
        # start-time
        for child in root.iter('programme'):
            starttime_pre = child.attrib['start']
            starttime = aslocaltimestr(datetime.strptime(starttime_pre[0:4]+"-"+starttime_pre[4:6] +"-"+starttime_pre[6:8]+"T"+starttime_pre[8:10]+":"+starttime_pre[10:12], '%Y-%m-%dT%H:%M')) + "; "
            if starttime is None:
                starttime = "1970-00-00T00:00; "
        # stop-time
        for child in root.iter('programme'):
            stoptime_pre = child.attrib['stop']
            stoptime = aslocaltimestr(datetime.strptime(stoptime_pre[0:4]+"-"+stoptime_pre[4:6] +"-"+stoptime_pre[6:8]+"T"+stoptime_pre[8:10]+":"+stoptime_pre[10:12], '%Y-%m-%dT%H:%M')) + "; "
    if stoptime is None:
        stoptime = "1970-00-00T00:00; "
    # show sub-title
    for child in root.iter('sub-title'):
        subtitle = child.text  + "; "
    if subtitle is None:
        subtitle = "none; "
    # show-image
    for child in root.iter('icon'):
        show_image = child.attrib['src']  + "; "
    if show_image is None:
        show_image = "http://chanlogos.xmltv.se/13thstreet.de.png; "
    # country
    for child in root.iter('country'):
        country = child.text + " | "
    if country is None:
        country = ""
    # release-date
    for child in root.iter('date'):   
        date = child.text
    if date is None:
        date = ""
    # category
    for child in root.iter('category'):
        category = " | " + child.text
    if category is None:
        category = ""
    print(channel+channelUrl+title+subtitle+starttime+stoptime+show_image+country+date+category)
