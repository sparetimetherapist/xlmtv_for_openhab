#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from xml.etree import ElementTree as ET
import codecs, argparse, os, sys

# meta
script_ver = 0.1
script_dec = "Extract informations from XMLTV data"

# cmd
cmd_get_all = "get_all"
cmd_get_channelid = "get_channelid"
cmd_get_channelname = "get_channelname"
cmd_get_logourl = "get_logourl"
cmd_get_starttime = "get_starttime"
cmd_get_stoptime = "get_stoptime"
cmd_get_stop = "get_stop"
cmd_get_stopextra = "get_stopextra"
cmd_get_stopextra2 = "get_stopextra2"
cmd_get_startstop = "get_startstop"
cmd_get_title = "get_title"
cmd_get_subtitle = "get_subtitle"
cmd_get_description = "get_description"
cmd_get_director = "get_director"
cmd_get_actor = "get_actor"
cmd_get_writer = "get_writer"
cmd_get_date = "get_date"
cmd_get_category = "get_category"

# initialize arguments
parser = argparse.ArgumentParser(description=script_dec, version=str(script_ver))
parser.add_argument("-t", "--target", dest="target", action="store", help="target XMLTV file",
                    required=True)
parser.add_argument("-c", "--command", dest="command", action="store",
                    choices=[cmd_get_all, cmd_get_channelid, cmd_get_channelname, cmd_get_logourl, cmd_get_starttime, cmd_get_stoptime, cmd_get_stop, cmd_get_stopextra, cmd_get_stopextra2, cmd_get_startstop, cmd_get_title, cmd_get_subtitle, cmd_get_description, cmd_get_director, cmd_get_date],
                    help="command to execute for XMLTV file", required=True)

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout) # Force script to output UTF-8

# execute stuff with given attributes
args = parser.parse_args()
if args.command == cmd_get_all:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('channel'):
        print(child.attrib['id'])
    for child in root.iter('display-name'):
        print(child.text)
    for child in root.iter('icon'):
        print(child.attrib['src'])    
    for child in root.iter('programme'):
        print(child.attrib['start'])
    for child in root.iter('programme'):
        print(child.attrib['stop'])
    for child in root.iter('title'):
        print(child.text)
    for child in root.iter('sub-title'):
        print(child.text)
    for child in root.iter('desc'):
        print(child.text)
    for child in root.iter('director'):
        print(child.text)
    for child in root.iter('date'):
        print(child.text)

if args.command == cmd_get_channelid:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('channel'):
        print(child.attrib['id'])

if args.command == cmd_get_channelname:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('display-name'):
        print(child.text)

if args.command == cmd_get_logourl:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('icon'):
        print(child.attrib['src'])

if args.command == cmd_get_starttime:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('programme'):
        startTime = child.attrib['start']
        print(startTime[0:4]+"-"+startTime[4:6] +"-"+startTime[6:8]+"T"+startTime[8:10]+":"+startTime[10:12])

if args.command == cmd_get_stoptime:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('programme'):
        stopTime = child.attrib['stop']
        print(stopTime[0:4]+"-"+stopTime[4:6] +"-"+stopTime[6:8]+"T"+stopTime[8:10]+":"+stopTime[10:12])

if args.command == cmd_get_stop:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('programme'):
        stop = child.attrib['stop']
        extra_time = datetime.strptime(stop[0:4]+"-"+stop[4:6] +"-"+stop[6:8]+"T"+stop[8:10]+":"+stop[10:12], '%Y-%m-%dT%H:%M')
        print(extra_time.strftime('%H:%M'))

if args.command == cmd_get_stopextra:
    tree = ET.parse(args.target)
    root = tree.getroot()
    data = []
    for child in root.iter('programme'):
        stop = child.attrib['stop']
        extra_time = datetime.strptime(stop[0:4]+"-"+stop[4:6] +"-"+stop[6:8]+"T"+stop[8:10]+":"+stop[10:12], '%Y-%m-%dT%H:%M')
        data.append(extra_time)
    print(min(data).strftime('%Y-%m-%dT%H:%M'))

if args.command == cmd_get_stopextra2:
    tree = ET.parse(args.target)
    root = tree.getroot()
    data = []
    for child in root.iter('programme'):
        stop = child.attrib['stop']
        extra_time = datetime.strptime(stop[0:4]+"-"+stop[4:6] +"-"+stop[6:8]+"T"+stop[8:10]+":"+stop[10:12], '%Y-%m-%dT%H:%M')
        data.append(extra_time)
    print(min(data).strftime('%H:%M'))

if args.command == cmd_get_startstop:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('programme'):
        startTime = child.attrib['start']
        stopTime = child.attrib['stop']
        print(startTime[8:10]+":"+startTime[10:12]+" - "+stopTime[8:10]+":"+stopTime[10:12])

if args.command == cmd_get_title:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('title'):
        print(child.text)

if args.command == cmd_get_subtitle:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('sub-title'):
        print(child.text)

if args.command == cmd_get_description:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('desc'):
        print(child.text)

if args.command == cmd_get_director:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('director'):
        print(child.text)

if args.command == cmd_get_date:
    tree = ET.parse(args.target)
    root = tree.getroot()
    for child in root.iter('date'):
        print(child.text)