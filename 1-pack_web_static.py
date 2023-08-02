#!/usr/bin/python3
"""
Module that generates a .tgz archive from the web_static directory
"""
import os.path as osp
from datetime import datetime as dt
from fabric.api import local


def do_pack():
    """
    A function that creates a .tgz archive file containing all the
    files in the web_static folder
    """
    date = dt.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(date.year,
                                                         date.month,
                                                         date.day,
                                                         date.hour,
                                                         date.minute,
                                                         date.second)
    if osp.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return (None)
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return (None)
    return (file)
