#!/usr/bin/env bash
#
# This script is supposed to be sourced (like `source setup_dev.sh`)
# by @mb6ockatf, Mon 27 Mar 2023 09:32:42 PM MSK

python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r requirements.txt

