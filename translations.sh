#!/bin/bash

# Simple script to generate translations starting from the app_strings.py file
if [[ $1 == "po" ]]; then
    xgettext -o translations/it/LC_MESSAGES/it.po --keyword="N_" -j app_strings.py
    xgettext -o translations/mn/LC_MESSAGES/mn.po --keyword="N_" -j app_strings.py
elif [[ $1 == "mo" ]]; then
    msgfmt -o translations/it/LC_MESSAGES/it.mo translations/it/LC_MESSAGES/it.po
    msgfmt -o translations/mn/LC_MESSAGES/mn.mo translations/mn/LC_MESSAGES/mn.po
else
    echo "Please provide either po or mo as argument of this script"
fi
