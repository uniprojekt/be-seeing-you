#!/bin/bash
python -m pypm init
python -m pypm add bsm "DISPLAY=:0 python ~/be-seeing-you/camera.py"
