#!/bin/sh
echo "checking to update files"
git pull
echo "starting cuneyt script"
python main.py
echo "done"
