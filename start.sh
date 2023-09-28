#!/bin/bash
cd ~/be-seeing-you
python -m pypm init
python -m pypm add bsm "DISPLAY=:0 python ./camera.py"
