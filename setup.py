# pylint: disable=invalid-name, unnecessary-pass, consider-using-with

"""
    Setup for apache beam pipeline.
"""

from __future__ import absolute_import
from __future__ import print_function
import subprocess
from distutils.command.build import build as _build  # type: ignore
import setuptools


# This class handles the pip install mechanism.
class build(_build):  # pylint: disable=invalid-name
    """A build command class that will be invoked during package install.
    The package built using the current setup.py will be staged and later
    installed in the worker using `pip install package'. This class will be
    instantiated during install for this specific scenario and will trigger
    running the custom commands specified.
    """
    sub_commands = _build.sub_commands + [('CustomCommands', None)]


CUSTOM_COMMANDS = [
    ["gsutil","cp" ,"gs://gdw-shared-resources/certs/*" ,"/usr/local/share/ca-certificates/"],
    ["sudo","update-ca-certificates"],
    ["gsutil" ,"cp", "gs://gdw-shared-resources/init/pip.conf", "/etc/pip.conf"],
    ["sudo","apt-get","--assume-yes", "update"],
#     ["pip","install","apache-beam[gcp]"],
    ["/usr/local/bin/python3" ,"-m", "pip" ,"install" ,"--upgrade", "pip"],
    ["pip","install","python-snappy"],
    ["pip","install","google-cloud-storage"],
    ["pip","install","google-api-python-client"],
    ["pip","install","google-api-client"],
    ["pip","install","google-cloud-aiplatform"],
    ["pip","install","fsspec"],
    ["pip","install" ,"dill==0.3.2"],
    ["pip","install","tensorflow"],
    ["pip","install","tfx==0.29.0"],
    ["pip","install","kfp==1.6.1"],
    ["pip","install","gcsfs"]
                  ]


class CustomCommands(setuptools.Command):
    """A setuptools Command class able to run arbitrary commands."""
    def initialize_options(self):
        """Initialize options"""
        pass

    def finalize_options(self):
        """Finalize options"""
        pass

    def RunCustomCommand(self, command_list):   # pylint: disable=no-self-use
        """To run custom command"""
        print('Running command: %s' % command_list)
        p = subprocess.Popen(
        command_list,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    # Can use communicate(input='y\n'.encode()) if the command run requires
    # some confirmation.
        stdout_data, _ = p.communicate()
        print('Command output: %s' % stdout_data)
        if p.returncode != 0:
            raise RuntimeError(
          'Command %s failed: exit code: %s' % (command_list, p.returncode))

    def run(self):
        """Run function for custom commands"""
        for command in CUSTOM_COMMANDS:
            self.RunCustomCommand(command)





NAME = 'Unified Ai Online'
VERSION = '2.0'
REQUIRED_PACKAGES = [
    'apache-beam[gcp]',
    'tensorflow==2.3.0',
    'opencv-python',
    'gcsfs',
    'workflow'
    ]

setuptools.setup(
    name=NAME,
    version=VERSION,
    install_requires=[],
    packages=setuptools.find_packages(),
    cmdclass={
        # Command class instantiated and run during pip install scenarios.
        'build': build,
        'CustomCommands': CustomCommands
    }
)
