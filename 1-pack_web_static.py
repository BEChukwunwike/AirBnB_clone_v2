#!/usr/bin/python3
"""A Fabric script that generates a .tgz archive from the contents of
web_static folder of the AirBnB Clone repo, using the function do_pack."""

from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """A function that creates a .tgz archive."""
    ver = datetime.now().strftime("%Y%m%d%H%M%S")
    if isdir("versions") is False:
        local("mkdir versions")
    file_version = "versions/web_static_{}.tgz".format(ver)
    archive = local("tar -cvzf {} web_static".format(file_version))
    if archive.succeeded:
        print("Test file")
        return file_version
    else:
        return None
