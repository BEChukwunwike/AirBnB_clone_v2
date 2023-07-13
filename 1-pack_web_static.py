#!/usr/bin/python3
"""A Fabric script that generates a .tgz archive from the contents of
web_static folder of the AirBnB Clone repo, using the function do_pack."""

from datetime import datetime
from fabric.api import local
from os.path import isdir
import os


def do_pack():
    """A function that creates a .tgz archive."""
    if isdir("versions") is False:
        local("mkdir versions")
    ver = datetime.now().strftime("%Y%m%d%H%M%S")
    file_version = "versions/web_static_{}.tgz".format(ver)
    print("Packing web_static to {}".format(file_version))
    archive = local("tar -cvzf {} web_static".format(file_version))
    size = os.stat(file_version).st_size
    print("web_static packed: {} -> {}Bytes".format(file_version, size))
    if archive.succeeded:
        return file_version
    else:
        raise Exception('None')
