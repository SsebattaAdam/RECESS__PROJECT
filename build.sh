#!/usr/bin/env bash
# exit on errore
set -o errexit

python -m pip install --upgrade pip

pip install -r requirements.txt
