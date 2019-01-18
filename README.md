# XMLTV for openHAB
Install and set-up xmltv to work with openHAB (early version)

This is just a simple install & configuration tool for xmltv -preconfigured for EU-channels- which is needed to import EPG-informations
into openHAB. (tested on openHABianPi v1.4.1 with openHAB 2.5.0 (Build #1495) installed)

## Prerequisites
- **xmltv** (see http://wiki.xmltv.org/index.php/Main_Page for details)
- **Python 2.7.x** (preinstalled on most systems)
- **openHAB 2.x** with the following bindings/transformations:
  - Exec Binding
  - NTP Binding
  - MAP Transformation
  - JavaScript Transformation

## Automatic install
1. Run install.sh
2. Copy the files from this repository to your openHAB environment
  - \rules\epg.rules
  - \items\epg.items
  - \sitemaps\epg.sitemap
  - \transform\epg.map
  - \transform\epg_duration.js
  - \scripts\epg_parser.py

## Manual install
1. Install xmltv `sudo apt-get install xmltv`

2. Create directories `sudo -u openhab mkdir -p /etc/openhab2/html/epg/{data/tmp,conf}`

3. Configure xmltv once (configured to use a grabber for EU channels) `sudo -u openhab printf 'http://xmltv.xmltv.se/channels.xml.gz\n/etc/openhab2/html/epg/data/tmp\nnone' | /usr/bin/tv_grab_eu_egon --configure --config-file /etc/openhab2/html/epg/conf/epg_eu.conf --quiet`

4. Change the timezone for the tv_grep (part of xmltv), if you´re not on UTC `sudo sed -i -e 's/UTC/CET/g' /usr/bin/tv_grep`

5. Select the channels you want to monitor, by changing '!' to '=' in the xmltv-conf `nano /etc/openhab2/html/epg/conf/epg_eu.conf`

6. Copy the files from this repository to your openHAB environment
  - \rules\epg.rules
  - \items\epg.items
  - \sitemaps\epg.sitemap
  - \transform\epg.map
  - \transform\epg_duration.js
  - \scripts\epg_parser.py

More details here: https://community.openhab.org/t/use-xmltv-with-openhab/60367
