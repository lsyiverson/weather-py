# -*- coding: utf-8 -*-
# encoding=utf-8
import os
import codecs
import shutil

def mkdir(path):
    path=path.strip()
    path=path.rstrip('/')

    isExists=os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        print path+' is created'
        return True
    else:
        print path+' is already existed'
        return False

def touch(filepath):
    filepath=filepath.strip()
    filepath=filepath.rstrip('/')

    isExists=os.path.exists(filepath)

    if not isExists:
        f = open(filepath, 'w')
        f.close()
        print filepath+' is created'
        return True
    else:
        print filepath+' is already existed'
        return False

def append(filepath, content):
    filepath=filepath.strip()
    filepath=filepath.rstrip('/')

    f = codecs.open(filepath, 'a', 'utf8')
    f.write(content)
    f.close()

def rmtree(dirpath):
    dirpath=dirpath.strip()
    dirpath=dirpath.rstrip('/')

    isExists=os.path.exists(dirpath)

    if isExists:
        shutil.rmtree(dirpath)
        print dirpath+' is deleted'
        return True
    else:
        return False