# encoding: utf-8
"Run a Python script."

__version__ = "$LastChangedRevision: 223 $"

import os

from waflib import Task, TaskGen, Logs
import re


def configure(ctx):
    """TODO: Needs updating for Windows once 
    "PEP 397":http://www.python.org/dev/peps/pep-0397/ is settled.
    
    """
    # Counter how many Python interpreters are found
    cnt = 0
    # Check for Python and Python3
    for cmd, var in ('python', 'PY2CMD'), ('python3', 'PY3CMD'):
        try:
            ctx.find_program(cmd, var=var)
            cnt += 1
        except ctx.errors.ConfigurationError:
            pass
    # Just a cautionary error -- should never happen (we wouldn't be here...)
    if cnt == 0:
        raise ctx.errors.ConfigurationError("No Python interpreter found!")


@Task.update_outputs
class RunPyScriptBase(Task.Task):
    """Base class for running Python scripts. Because of the upate outputs
    decorator, the MD5-checksums of the target files will be used for further
    dependency checking. 
    
    """

    def scan(self):
        """Process the *deps* attribute of the task generator. Shamelessly
        copied from TaskGen.process_rule.
        
        """

        nodes = []
        for x in self.generator.to_list(getattr(self.generator, 'deps', '')):
            node = self.generator.path.find_resource(x)
            if not node:
                self.generator.bld.fatal('Could not find %r (was it declared?)' % x)
            nodes.append(node)
        return (nodes, [])

    def run(self):
        Logs.debug('runner: {} on {}'.format(self.py_cmd_str(), self.inputs[0].abspath))
        # Pass the environment on.
        self.env.env = os.environ
        # Make sure PYTHONPATH attribute is present
        self.env.env['PYTHONPATH'] = self.env.env.get('PYTHONPATH', '')
        # Add stuff from the project paths 
        project_paths = getattr(self.env, 'PROJECT_PATHS', None)
        if project_paths and 'PROJECT_ROOT' in project_paths:
            self.env.env['PYTHONPATH'] += os.pathsep + project_paths['PROJECT_ROOT'].abspath()
        # Add manual extensions to PYTHONPATH.
        if getattr(self.generator, 'add_to_pythonpath', None):
            self.env.env['PYTHONPATH'] += os.pathsep + self.generator.add_to_pythonpath
        # Clean up the PYTHONPATH -- replace double occurrences of path separator 
        self.env.env['PYTHONPATH'] = re.sub(os.pathsep + '+', os.pathsep, self.env.env['PYTHONPATH'])
        # Clean up the PYTHONPATH -- doesn't like starting with path separator
        if self.env.env['PYTHONPATH'].startswith(os.pathsep):
             self.env.env['PYTHONPATH'] = self.env.env['PYTHONPATH'][1:]
        # Run the Python script.
        ret = self.py_fun()(self)
        if ret:
            Logs.error('Running {} on {} returned a non-zero exit.'.format(self.py_cmd_str(), self.inputs[0]))
        return ret


class RunPy2Script(RunPyScriptBase):
    """Subclass to run a Python 2 script."""

    def py_cmd_str(self):
        return self.env.PY2CMD

    def py_fun(self):
        in_script = self.inputs[0].abspath()
        fun_str = '{} {}'.format(self.env.PY2CMD, in_script)
        return Task.compile_fun(fun_str, shell=True)[0]


class RunPy3Script(RunPyScriptBase):
    """Subclass to run a Python 3 script."""

    def py_cmd_str(self):
        return self.env.PY3CMD

    def py_fun(self):
        in_script = self.inputs[0].abspath()
        fun_str = '{} {}'.format(self.env.PY3CMD, in_script)
        return Task.compile_fun(fun_str, shell=True)[0]


@TaskGen.feature('run_py_script')
@TaskGen.before_method('process_source')
def apply_run_py_script(tsk_g):
    """Task generator for running either Python 2 or Python 3 on a single
    script. 
    
    Attributes:
        * source -- A **single** source node or string. (required)
        * target -- A single target or list of targets (nodes or strings). 
        * deps -- A single dependency or list of dependencies (nodes or strings)
        * add_to_pythonpath -- A string that will be appended to the PYTHONPATH
                               environment variable.
    
    Note that if the build environment has an attribute "PROJECT_PATHS" with
    a key "PROJECT_ROOT", its value will be appended to the PYTHONPATH. 
    
    """

    # Set the Python version to use, default to 3.
    v = getattr(tsk_g, 'version', 3)
    if v not in {2, 3}: raise ValueError(
        "Specify the 'version' attribute for run_py_script task "
        "generator as integer 2 or 3.\n Got: {}".format(v))

    # Convert sources and targets to nodes 
    src_node = tsk_g.path.find_resource(tsk_g.source)
    tgt_nodes = [tsk_g.path.find_or_declare(t) for t in tsk_g.to_list(tsk_g.target)]

    # Create the task.
    tsk_g.create_task('RunPy{}Script'.format(v), src=src_node, tgt=tgt_nodes)

    # Bypass the execution of process_source by setting the source to an empty list
    tsk_g.source = []
