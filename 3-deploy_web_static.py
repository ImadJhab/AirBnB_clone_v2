#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers
"""
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
import os
env.hosts = ['3.90.81.20', '54.84.14.76']


def do_pack():
    """Function to generate a .tgz archive from web_static folder."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """deploys archive to server"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception:
        return False


def deploy():
    """ do path and do the deploy"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
