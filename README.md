# Plex-Auto-Updater
Plex Auto-Updater checks if your current server is up to date, and will install the latest update if not.

## Prerequisites
* Debian-based server running Plex Media Server
* Python 3 with the [PlexAPI](https://github.com/pkkid/python-plexapi) installed. (`pip3 install plexapi`)

## How To Use
Run the plex-updater.py script with root permissions. The script requires four positional arguments, the server name, server architecture and username/password of any user with access to the server. Use `plex-updater.py --help` for more information. 

Sample Usage:
`sudo python3 plex-updater.py MyServer AMD-64 myname MY_P455W0RD`

## Setting Up Automated Updates
The `plex-updater.py` script will run only once, in order to have automated updates you should set up a cron job on your machine which will run the script at whatever frequency you'd like. Remember, Plex will be unavailable while the update installs (usually less than 2 minutes). More information on cron jobs can be found [here](https://lmgtfy.com/?iie=1&q=cron+job+for+python).
