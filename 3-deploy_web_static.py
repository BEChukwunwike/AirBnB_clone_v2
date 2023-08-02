#!/usr/bin/python3
"""
Module that generates a .tgz archive from the web_static directory
Uploads the archive file to the web servers.
"""
import os.path as osp
from datetime import datetime as dt
from fabric.api import local
from fabric.api import env
from fabric.api import run
from fabric.api import put

"""setting the environment host for the servers"""
env.hosts = ['18.209.180.65', '18.204.15.209']


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


def do_deploy(archive_path):
    """
    A function that distributes an archive file to a web server

    Args:
        archive_path (str): path to the archive to distribute

    Returns:
        True if the archive path exist and there is no error
        Otherwise - False
    """
    if osp.isfile(archive_path) is False:
        return (False)
    file = archive_path.split("/")[-1]
    fn = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return (False)

    if run("sudo rm -rf /data/web_static/releases/{}/".
            format(fn)).failed is True:
        return (False)

    if run("sudo mkdir -p /data/web_static/releases/{}/".
            format(fn)).failed is True:
        return (False)

    if run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, fn)).failed is True:
        return (False)

    if run("sudo rm /tmp/{}".format(file)).failed is True:
        return (False)

    if run("sudo mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(fn, fn)).failed is True:
        return (False)

    if run("sudo rm -rf /data/web_static/releases/{}/web_static".
           format(fn)).failed is True:
        return (False)

    if run("sudo rm -rf /data/web_static/current").failed is True:
        return (False)

    if run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(fn)).failed is True:
        return (False)

    return True


def deploy():
    """
    This function creates and distributes a codebase archive to the webserver
    """
    codeBase_file = do_pack()
    if codeBase_file is None:
        return (False)
    return (do_deploy(codeBase_file))
