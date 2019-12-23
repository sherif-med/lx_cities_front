#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 10:10:33 2019

@author: cherif
"""

from session import db_session, base_classes
from wtforms_alchemy import model_form_factory
from wtforms import StringField, SubmitField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

# Inputs validators
from formsValidators import validate_file_exists
from utils import get_shape_from_s3, get_cities, get_class_features_factory
from shapely.geometry import shape

######################### Defining Forms models ###############################

from flask_wtf import Form as FlaskForm
BaseModelForm = model_form_factory(FlaskForm)
class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db_session


################################ Base_classes keys ############################

# ['cities', 'class_feature', 'image_file', 'update', 'cropped_images', 'catalog_image']

######################### Defining Forms models ###############################
        
############################## CityForm ######################################
class CityForm(ModelForm):
    class Meta:
        model = base_classes["cities"]
    foot_print_file_location = StringField('foot_print file location', validators=[DataRequired(), validate_file_exists])
        
    submit = SubmitField()
    
    def get_footprint_data(self, foot_print_file_location):
        """
        loads shapefile from s3 and returns a tuple of projection string and geometry wkt string
        """
        collection = get_shape_from_s3(foot_print_file_location)
        geom = shape(collection[0]["geometry"])
        return "EPSG:4326", geom.wkt

############################## ClassFeatureForm ##############################
class ClassFeatureForm(ModelForm):
    class Meta:
        model = base_classes["class_feature"]
    respective_city = QuerySelectField("Respective city", query_factory=get_cities, get_label='full_name')
    # Defining choices
    features_choices = [('raw', 'Raw images'), ('building', 'Building shape'), ('tree', 'tree shape')]
    feature_name = SelectField('feature type', choices=features_choices)
    
    submit = SubmitField()


############################## ClassFeatureForm ##############################
class ImageFileForm(ModelForm):
    class Meta:
        model = base_classes["image_file"]
    respective_city = QuerySelectField("Respective city", query_factory=get_cities, get_label='full_name')
    respective_feature = QuerySelectField("Respective feature class", query_factory=get_class_features_factory(respective_city.data.id), get_label='name')
    image_file_location = StringField('image file location', validators=[DataRequired(), validate_file_exists])
    
    submit = SubmitField()




