#!/usr/bin/python3
"""A Fabric script that
1. archives the content of web_static, using the function do_pack.
2. distributes an archive to your web servers, using the function do_deploy.
3. creates and distributes an archive to the web servers, using the function
    deploy.
4. deletes out-of-date archives, using the function do_clean.
"""

from datetime import datetime
from fabric.api import local
from fabric.api import put
from fabric.api import run
from fabric.api import env
from fabric.api import lcd
from fabric.api import cd
from os.path import isdir
from os.path import exists
import os

env.user = "ubuntu"
env.hosts = ['34.224.95.183', '100.26.224.205']


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


def do_deploy(archive_path):
    """A function that distributes an archive to the web servers."""
    if exists(archive_path) is False:
        return False
    zip_file = archive_path.split("/")[-1]
    version = zip_file.split(".")[0]
    path = "/data/web_static/releases/"
    if put(archive_path, "/tmp/{}".format(zip_file)).failed is True:
        print("Failed to upload archive file to /tmp/")
        return False
    if run("mkdir -p {}{}/".format(path, version)).failed is True:
        print("Failed to create file version")
        return False
    if run("tar -xzf /tmp/{} -C {}{}/"
           .format(zip_file, path, version)).failed is True:
        print("Failed to extract archive")
        return False
    if run("rm /tmp/{}".format(zip_file)).failed is True:
        print("Failed to delete archive")
        return False
    if run("mv {0}{1}/web_static/* {0}{1}/"
           .format(path, version)).failed is True:
        print("Failed to reposition web_static content")
        return False
    if run("rm -rf {}{}/web_static".format(path, version)).failed is True:
        print("Failed to delete web_static folder")
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        print("Failed to remove old symlink")
        return False
    if run("ln -s {}{}/ /data/web_static/current"
           .format(path, version)).failed is True:
        print("Failed to create symlink for deploying web content")
        return False
    print("New version deployed!")
    return True


def deploy():
    """A function that creates and distributes an archive to the web servers,
    using the function deploy"""
    archive = do_pack()
    if archive is None:
        return False
    return do_deploy(archive)


def do_clean(number=0):
    """A function that deletes out-of-date archives, using the function
    do_clean
    Arg: number (int): the number of the archives, including the most recent,
    to keep
    """
    number = 1 if int(number) == 0 else int(number)
    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(arch)) for arch in archives]
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
