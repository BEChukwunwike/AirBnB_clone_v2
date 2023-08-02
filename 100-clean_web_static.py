#!/usr/bin/python3
"""Module to delete out-of-date archives"""
import os
from fabric.api import *

"""setting the environment host for the servers"""
env.hosts = ['18.209.180.65', '18.204.15.209']


def do_clean(number=0):
    """
    This is a method/function that removes outdated archives

    Args:
        number (int): The number of archives to keep
    Description:
        If number = 0 || 1, keep only the most recent archive
        if number is 2, keep the 2 most recent archives
    Returns:
        Nothing
    """
    number = 1 if int(number) == 0 else int(number)

    zipfiles = sorted(os.listdir("versions"))
    [zipfiles.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for zipfile in zipfiles]

    with cd("/data/web_static/releases"):
        zipfiles = run("ls -tr").split()
        zipfiles = [a for zipfile in zipfiles if "web_static_" in zipfile]
        [zipfiles.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for zipfile in zipfiles]
