#!/usr/bin/env python

# standard library
import os
import glob
import stat
import shutil
import fnmatch

top = '.'
out = '.bld'

def options(opt):

    opt.load('compiler_c')

    opt.load('compiler_fc')

def configure(conf):

    conf.env.project_paths = {}

    conf.env.project_paths['MAIN'] = os.getcwd()
    
    conf.env.project_paths['STRUCT_TOOLBOX'] = os.getcwd()

    tools_dir = conf.env.project_paths['STRUCT_TOOLBOX'] + '/tools/computation/msc'

    conf.load('runPyScript', tooldir = tools_dir)
    
    conf.load('compiler_fc')

def build(bld):
    
    bld.env.PROJECT_PATHS = set_project_paths(bld)

    os.chdir(bld.env.project_paths['STRUCT_TOOLBOX'])

    set_permissions()

    bld.recurse('tools/computation/f90')

    bld.add_group() 

    bld.recurse('tests')

def distclean(ctx):
    
    remove_filetypes_distclean('.')

    remove_for_distclean('.waf-1.6.4-8c7ad4bb8e1ca65b04e5d8dd9d0dac54')

    remove_for_distclean('.bld')

    remove_for_distclean('tools/computation/f90/include')

    remove_for_distclean('tools/computation/f90/lib')
    
''' Auxiliary functions.
'''
def set_permissions():
    ''' Set permissions.
    '''
    
    files = glob.glob('scripts/*.py')

    for file_ in files:
        
        os.chmod(file_, 0777)
    
def remove_for_distclean(path):
    ''' Remove path, where path can be either a directory or a file. The
        appropriate function is selected. Note, however, that if an 
        OSError occurs, the function will just path.
    '''

    if os.path.isdir(path):

        shutil.rmtree(path)
    
    if os.path.isfile(path):

        os.remove(path)

def remove_filetypes_distclean(path):
    ''' Remove nuisance files from the directory tree.

    '''

    matches = []

    for root, _, filenames in os.walk('.'):

        for filetypes in ['*.aux','*.log','*.pyc', '*.so', '*~', '*tar', \
            '*.zip', '.waf*', '*lock*', '*.mod', '*.a', '*.pkl', '*.out', '*.pyo', '*.info']:

                for filename in fnmatch.filter(filenames, filetypes):
                    
                    matches.append(os.path.join(root, filename))

    matches.append('.lock-wafbuild')
    
    matches.append('doc/.build')

    for files in matches:

        remove_for_distclean(files)

def set_project_paths(ctx):
    ''' Return a dictionary with project paths represented by Waf nodes. This is
        required such that the run_py_script works as the whole PROJECT_ROOT is
        added to the Python path during execution.
    ''' 

    pp = {}

    pp['PROJECT_ROOT'] = '.'
   
    for key, val in pp.items():

        pp[key] = ctx.path.make_node(val)
   
    return pp

