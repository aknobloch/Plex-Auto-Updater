import argparse
import requests
import sys
from plexapi.myplex import MyPlexAccount
import subprocess
import os

if __name__ != '__main__':

    log.error('Plex Auto-Updater not called directly, exiting...')
    sys.exit(1)

parser = argparse.ArgumentParser(
    prog='Plex Auto-Updater',
    usage='sudo python3 plex-updater.py MyServer AMD-64 aknobloch MY_P455W0RD',
    description='Enables automated updates for the Plex Media Server.')

parser.add_argument(
    'server_name',
    metavar='server',
    type=str,
    help='Name of the Plex server. This can be found by logging into \
        the desired server via the Web UI. The name will be in the upper left.')

parser.add_argument(
    'server_architecture',
    metavar='architecture',
    type=str,
    help='Architecture of the Plex server. This will be one of the following: \
        AMD-32 (32 bit), AMD-64 (64 bit), ARMv8 or ARMv7')

parser.add_argument(
    'username',
    metavar='username',
    type=str,
    help='Username for the owner of the Plex server.')

parser.add_argument(
    'password',
    metavar='password',
    type=str,
    help='Password for the owner of the Plex server.')

args = parser.parse_args()

username = args.username
password = args.password
server_name = args.server_name
server_architecture = args.server_architecture

# Key corresponds to the option given when running the script
# The value is the associated text which is appended to the
# request URL when pulling the latest images.
valid_architectures = {
    'AMD-32':'i386',
    'AMD-64':'amd64',
    'ARMv8':'arm64',
    'ARMv7':'armhf'
}

if(server_architecture not in valid_architectures) :
    print('Architecture {} is not recognized.'.format(server_architecture))
    print('Please supply one of the following:')
    print(*valid_architectures.keys(), sep = ", ")
    sys.exit(1)
else :
    # Map the server architecture to the internal-use value
    server_architecture = valid_architectures[server_architecture]

# Validate script is being run with root permissions
if(os.geteuid() != 0) :
    print('Plex Auto-Updater must be run with root permissions.')
    sys.exit(1)

# Login and get server information
account = MyPlexAccount(username, password)
plex = account.resource(server_name).connect()
print('Current Plex installation is version {}, running on {}.'.format(plex.version, plex.platform))

# Get latest release information
release_info_request = requests.get('https://plex.tv/api/downloads/5.json')

if(release_info_request.status_code != 200) :
    print('Unable to fetch latest Plex release information.')
    sys.exit(1)

release_info = release_info_request.json()
latest_version = release_info['computer'][plex.platform]['version']

# Check if up to date
if(latest_version is None or latest_version == '') :
    print('Unable to determine latest version for your platform.')
    print('NOTE: Plex Auto-Updater does not support NAS devices.')
    sys.exit(1)
else :
    print('Latest Plex release is version {}.'.format(latest_version))

if(plex.version.lower() == latest_version.lower()) :
    print('Plex is up to date.')
    sys.exit(0)

# Pull latest release down
release_url = 'https://downloads.plex.tv/plex-media-server-new/{}/debian/plexmediaserver_{}_{}.deb'.format(latest_version, latest_version, server_architecture)
latest_release = requests.get(release_url)

if(latest_release.status_code != 200 or latest_release.content is None) :
    print('Unable to fetch latest Plex release.')
    sys.exit(1)

filename = 'plex_release_{}.deb'.format(latest_version)
open(filename, 'wb').write(latest_release.content)

# Install latest version
install_result = subprocess.run(['dpkg', '-i', filename])

if(install_result.returncode != 0) :
    print('Failed to install latest Plex version.')
    sys.exit(1)

# Cleanup file
os.remove(filename)
