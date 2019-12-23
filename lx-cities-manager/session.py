#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 09:02:14 2019

@author: cherif
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from decouple import config

lx_cities_db_uri = config('DATABASE_URL')

base_classes = dict()

def get_db_session(uri):
    """
    """
    Base = automap_base()
    
    engine = create_engine(uri)
    
    # reflect the tables
    Base.prepare(engine, reflect=True)
    
    # mapped classes are now created with names by default
    # matching that of the table name.
    for base_class in Base.classes:
        base_classes.update({base_class.__name__ : base_class})
        # forms_classes.update(define_form_class(base_class.__name__, base_class))
    
    db_session = Session(engine)
    
    return db_session

db_session = get_db_session(lx_cities_db_uri)
