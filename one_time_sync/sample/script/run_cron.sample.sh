#!/bin/sh

# Set-up keychain environnement
SHELL=/bin/sh
eval `keychain --noask --quiet --eval id_dsa`

# Set-up python environnement
export PYTHONIOENCODING=UTF-8
PYTHON3=/usr/local/bin/python3

${PYTHON3} -m one_time_sync --config YOUR_ABSOLUTE_PATH_TO_CONFIG
