#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 14:24:31 2019

@author: cherif
"""

import os

class Config(object):
    SECRET_KEY = os.urandom(32) or 'you-will-never-guess'