#!/bin/sh
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "               .__   __         "
echo "___  ___ _____ |  |_/  |____  __"
echo "\  \/  //     \|  |\   __\  \/ /"
echo " >    <|  Y Y  \  |_|  |  \   / "
echo "/__/\_ \__|_|  /____/__|   \_/   Installer for OH2.x"
echo "      \/     \/                 "
echo -e "${RED}Experimental${NC} - only for testing purposes"
echo ""

echo -ne "Checking user privileges... \r"

# Checking for sudo privileges
if [ "$EUID" -ne 0 ]
then 
    echo -e "${RED}Error: ${NC}Please run as root"
    echo ""
    exit
fi

# Check if user 'openhab' exists
if [ $(id -u openhab > /dev/null 2>&1; echo $?)  == 0 ]
then
    echo "User 'openhab exists - proceed...'" &> /dev/null
else
    echo -e "${RED}Error: ${NC}There is no user 'openhab' on your system. Use --help for further instructions."
    echo ""
    exit
fi

echo -ne "Checking user privileges ${GREEN}[DONE]${NC} \n"

# Updating system, install xmltv & get python-script from git
echo -ne "Updating system and install xmltv... \r"
sudo apt-get update  &> /dev/null
sudo apt-get install xmltv -y  &> /dev/null
echo -ne "Updating system and install xmltv ${GREEN}[DONE]${NC} \n"

# Creating needed directories with user 'openhab'
echo -ne "Creating directories... \r"
DESTINATION="/etc/openhab2/html/epg"
sudo -u openhab mkdir -p ${DESTINATION}/{data/tmp,conf} &> /dev/null
echo -ne "Creating directories ${GREEN}[DONE]${NC} \n"

# Start configuring grabber
echo -ne "Configuring grabber... \r"
sudo printf 'http://xmltv.xmltv.se/channels.xml.gz\n/etc/openhab2/html/epg/data/tmp\nnone' | /usr/bin/tv_grab_eu_egon --configure --config-file /etc/openhab2/html/epg/conf/epg_eu.conf --quiet &> /dev/null
echo -ne "Configuring grabber ${GREEN}[DONE]${NC} \n"

# Checking local timezone
echo -ne "Configuring timezone... \r"

if [ $(date +%Z) == "CET" ]
then
    sudo sed -i -e 's/UTC/CET/g' /usr/bin/tv_grep
    echo -ne "Configuring timezone ${GREEN}[DONE]${NC} \n"
else 
    echo "No timezone-changes made..."
fi

echo ""
echo -e "${GREEN}Installation complete.${NC}"
echo "Now edit your xmltv-settings, using your favourite editor: /etc/openhab2/html/epg/conf/epg_eu.conf"
echo ""