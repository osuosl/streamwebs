#!/bin/bash
if [ $# -lt 2 ]; then
    python manage_dev_accounts.py $1
else
    python manage_dev_accounts.py $1 "${@:2}"
fi