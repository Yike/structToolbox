#!/usr/bin/env python
''' This script provisions the required software environment to run
	the structToolbox.
'''

# standard library
import os



packages = ['libblas-dev', 'liblapack-dev', 'gfortran']


for package in packages:

    os.system('sudo apt-get install -y ' + package)