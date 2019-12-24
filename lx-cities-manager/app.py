#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 09:58:27 2019

@author: cherif
"""

from session import db_session, base_classes
from formsModels import CityForm, ClassFeatureForm, ImageFileForm

from flask import Flask, url_for, render_template, redirect, jsonify, request
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
        # Set feature name
        feature_obj.name = class_feature_form.feature_name.data
        # Set respective city id
        feature_obj.resp_city= class_feature_form.respective_city.data.id
        db_session.add(feature_obj)
        db_session.commit()
        return redirect('/success')
    return render_template('classFeature/new.html', form=class_feature_form)

from utils import get_class_features_factory
@app.route('/_get_class_features')
def _get_class_features():
    city_id = request.args.get('city_id', type=int)
    class_features_for_city = get_class_features_factory(city_id)
    class_features_for_city = [(f.id, f.name) for f in class_features_for_city]
    return jsonify(class_features_for_city)

@app.route('/imageFile', methods=('GET', 'POST',))
def imageFile():
    image_file_form = ImageFileForm()    
    if image_file_form.validate_on_submit():
        print("*"*10)
        print(image_file_form.get_image_file_footprint_data())
        return redirect('/success')
        # Empty instance
        image_file_obj = base_classes["image_file"]()
        # Set city respective feature
        image_file_obj.resp_class_feature = image_file_form.respective_feature.data.id
        # Set image file type
        if (image_file_form.respective_feature.data.name == "raw"):
            image_file_obj.image_file_type = "raster"
        else:
            image_file_obj.image_file_type = "vector"
        # Set city footprint and projection
        image_file_obj.image_file_location= image_file_form.image_file_location.data
        # Set footprint
        image_file_obj.footprint, image_file_obj.footprint_wkt_proj = image_file_form.get_image_file_footprint_data()
        db_session.add(image_file_obj)
        db_session.commit()
        return redirect('/success')
    return render_template('imageFile/new.html', form=image_file_form)


if __name__ == '__main__':
    app.run(debug=True)