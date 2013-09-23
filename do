#!/bin/bash
python my_modify.py
NOW=$(date +"%y.%m.%d.%h.%M.%s")
mv niceout.wav ~/Downloads/$NOW.wav

