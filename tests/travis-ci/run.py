#!/usr/bin/env python
''' This script provisions the required software environment to run
	the structToolbox.
'''

import os

#
os.system('./waf configure build --test')

os.system('./waf configure build --test --speed')