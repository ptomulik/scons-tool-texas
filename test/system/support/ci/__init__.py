# -*- coding: utf-8 -*-
import os

def extend_path(env):
    try:
        path = os.environ['SCONS_PREPEND_PATH']
    except KeyError:
        pass
    else:
        env.PrependENVPath('PATH', path)
    try:
        path = os.environ['SCONS_APPEND_PATH']
    except KeyError:
        pass
    else:
        env.AppendENVPath('PATH', path)

def generate(env):
    extend_path(env)

def exists(env):
    return 1
