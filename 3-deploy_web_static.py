#!/usr/bin/python3
"""A Fabric script that
1. archives the content of web_static, using the function do_pack.
2. distributes an archive to your web servers, using the function do_deploy.
"""

from datetime import datetime
from fabric.api import local, put, run, env
from os.path import isdir, exists


def do_pack():
    """A function that creates a .tgz archive."""
    try:
        ver = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_version = "versions/web_static_{}.tgz".format(ver)
        local("tar -cvzf {} web_static".format(file_version))
        return file_version
    except:
        return None


def do_deploy(archive_path):
    """A function that distributes an archive to the web servers."""
    if exists(archive_path) is False:
        return False
    try:
        file_nm = archive_path.split("/")[-1]
        no_ext = file_nm.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_nm, path, no_ext))
        run('rm /tmp/{}'.format(file_nm))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
