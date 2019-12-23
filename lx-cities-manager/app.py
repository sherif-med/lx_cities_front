#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 09:58:27 2019

@author: cherif
"""

from session import db_session, base_classes
from formsModels import CityForm, ClassFeatureForm

from flask import Flask, url_for, render_template, redirect
app = Flask(__name__, instance_relative_config=False)

from config import Config
app.config.from_object(Config)

@app.route("/success")
def success():
    return "success"

@app.route('/city', methods=('GET', 'POST',))
def city():
    city_form = CityForm()
    if city_form.validate_on_submit():
        # Empty instance
        city_obj = base_classes["cities"]()
        # Set city full name
        city_obj.full_name = city_form.full_name.data
        # Set city footprint and projection
        city_obj.footprint_wkt_proj, city_obj.footprint = city_form.get_footprint_data(city_form.foot_print_file_location.data)
        db_session.add(city_obj)
        db_session.commit()
        return redirect('/success')
    return render_template('city/new.html', form=city_form)


@app.route('/feature', methods=('GET', 'POST',))
def feature():
    class_feature_form = ClassFeatureForm()
    if class_feature_form.validate_on_submit():
        # Empty instance
        feature_obj = base_classes["class_feature"]()
        # Set city full name
        feature_obj.name = class_feature_form.feature_name.data
        # Set city footprint and projection
        feature_obj.resp_city= class_feature_form.respective_city.data.id
        db_session.add(feature_obj)
        db_session.commit()
        return redirect('/success')
    return render_template('classFeature/new.html', form=class_feature_form)


if __name__ == '__main__':
    app.run(debug=True)