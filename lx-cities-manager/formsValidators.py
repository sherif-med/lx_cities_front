#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 14:18:37 2019

@author: cherif
"""

from wtforms.validators import ValidationError
from utils import check_file_exits



def validate_file_exists(form, field):
    # get_shape_from_s3(field.data)
    if not check_file_exits(field.data):
        raise ValidationError('File Not found')