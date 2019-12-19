#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 14:16:02 2019

@author: cherif
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sprox.formbase import AddRecordForm

lx_cities_db_uri = "postgres://postgres:MoroubaD8201@lxdb.chl8cpmnoyrm.us-east-1.rds.amazonaws.com:5432/usa"

base_classes = dict()
forms_classes = dict()


def define_form_class(base_class_name, base_class):
    class form(AddRecordForm):
        __model__ = base_class
    return { base_class_name.capitalize()+"Form" : form }

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
        forms_classes.update(define_form_class(base_class.__name__, base_class))
    
    db_session = Session(engine)
    
    return db_session

db_session = get_db_session(lx_cities_db_uri)

######################

from sqlalchemy.ext.declarative import declarative_base
DeclarativeBase = declarative_base()
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relation
class Genre(DeclarativeBase):
    __tablename__ = "genres"
    genre_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(200))

class Movie(DeclarativeBase):
    __tablename__ = "movies"
    movie_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    genre_id = Column(Integer, ForeignKey('genres.genre_id'))
    genre = relation('Genre', backref='movies')
    release_date = Column(Date, nullable=True)

class NewMovieForm(AddRecordForm):
    __model__ = Movie
new_movie_form = NewMovieForm(db_session)

#######################


from tg import expose, TGController, AppConfig, tmpl_context

new_city_form = forms_classes["CitiesForm"](db_session)

class RootController(TGController):
    @expose('new.xhtml')
    def new(self, **kw):
        tmpl_context.widget = new_city_form
        return dict(value=kw)
    
    @expose('new.xhtml')
    def old(self, **kw):
        tmpl_context.widget = new_movie_form
        return dict(value=kw)


    
    @expose()
    def index(self):
        return 'Hello World'
    
    @expose('templates.hello.xhtml')
    def hello(self, person=None):
        return dict(person=person)

    
config = AppConfig(minimal=True, root_controller=RootController())
config.renderers = ['kajiki']
application = config.make_wsgi_app()
from tw2.core.middleware import TwMiddleware
application = TwMiddleware(application)

from wsgiref.simple_server import make_server
httpd = make_server("", 8080, application)
httpd.serve_forever()