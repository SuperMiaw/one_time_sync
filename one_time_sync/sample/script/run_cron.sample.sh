#!/bin/sh

# Set-up keychain environnement
SHELL=/bin/sh
eval `keychain --noask --quiet --eval id_dsa`

# Set-up python environnement
export PYTHONIOENCODING=UTF-8
PYTHON27=/usr/local/bin/python2.7

${PYTHON27} -m one_time_sync --config YOUR_ABSOLUTE_PATH_TO_CONFIG
