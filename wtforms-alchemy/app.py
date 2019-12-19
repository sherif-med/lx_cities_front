#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:39:08 2019

@author: cherif
"""

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from wtforms_alchemy import ModelForm, ModelFieldList, ModelFormField
from wtforms.fields import FormField, FieldList

lx_cities_db_uri = "postgres://postgres:MoroubaD8201@lxdb.chl8cpmnoyrm.us-east-1.rds.amazonaws.com:5432/usa"

base_classes = dict()
forms_classes = dict()


def define_form_class(base_class_name, base_class):
    class form(ModelForm):
        class Meta:
            model = base_class
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


from flask import Flask, url_for, render_template, redirect
app = Flask(__name__, instance_relative_config=False)

@app.route('/city', methods=('GET', 'POST'))
def city():
    city_form = forms_classes["CitiesForm"]()
    class_feature_form = forms_classes["Class_featureForm"]
    city_form.class_features = ModelFieldList(FormField(class_feature_form, min_entries=2))
    city_form.class_features.append_entry()
    city_form.class_features.append_entry()
    print(city_form.class_features)
    """
    if form.validate_on_submit():
        return redirect(url_for('success'))
    """
    return render_template('index.html', form=city_form)

#######################################
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = 'event'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode(255), nullable=False)


class Location(Base):
    __tablename__ = 'location'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(255), nullable=True)

    event_id = sa.Column(sa.Integer, sa.ForeignKey(Event.id))
    event = sa.orm.relationship(
        Event,
        backref='locations'  # the event needs to have this
    )


class LocationForm(ModelForm):
    class Meta:
        model = Location


class EventForm(ModelForm):
    class Meta:
        model = Event

    locations = ModelFieldList(FormField(LocationForm, min_entries=2))

@app.route('/trial', methods=('GET', 'POST'))
def trial():
    city_form = EventForm()
    """
    if form.validate_on_submit():
        return redirect(url_for('success'))
    """
    return render_template('index.html', form=city_form)

if __name__ == '__main__':
    app.run(debug=True)