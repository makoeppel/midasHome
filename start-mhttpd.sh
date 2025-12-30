#!/bin/bash
set -e

# Load pi environment
source /home/pi/midasHome/midas.env

# Start mhttpd (daemon mode)
exec /home/pi/midas/bin/mhttpd

