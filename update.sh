#!/bin/sh
echo "stopping cuneyt main execution"

kill $(pgrep -f 'python main.py')

echo "checking to update files"

git pull

echo "restarting cuneyt script"

python main.py

echo "done"
