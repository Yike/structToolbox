#!/usr/bin/env python
''' This script provisions the required software environment to run
	the structToolbox.
'''

# standard library
import os



packages = ['gfortran', 'python3-dev', 'python3-numpy', 'python3-scipy', 'python3-pandas',
				'python3-setuptools', 'python3-pip', 'python3-nose', 'git']


#for package in packages:

#    os.system('sudo apt-get install -y ' + package)