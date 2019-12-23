#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 14:51:24 2019

@author: cherif
"""

import fiona
from decouple import config
import boto3
from session import db_session, base_classes

aws_access_key_id = config('AWS_ACCESS_KEY_ID')
aws_secret_access_key = config('AWS_SECRET_ACCESS_KEY')
S3_session_token = config('S3_SESSION_TOKEN')

def get_shape_from_s3(file_location):
    """
    Loads esri shape file from s3.
    Args:
        file_location : example: s3://bucket/file.shp
    Returns:
        fiona_collection : fiona object conatining features
    """
    fiona_collection = []
    with fiona.Env(session = fiona.session.AWSSession( 
                     aws_access_key_id = aws_access_key_id,
                     aws_secret_access_key = aws_secret_access_key,
                     aws_session_token=S3_session_token)):
        print(f"Loading file {file_location}")
        fiona_collection = fiona.open(file_location, driver="'ESRI Shapefile'")
    return fiona_collection

def get_cities():
    """
    Query db for existant cities
    """
    cities = db_session.query(base_classes["cities"])
    return cities



def get_class_features_factory(city_id):
    """
    a factory to generate methods for respective city_id
    """
    def get_class_features(city_id):
        """
        Query db for class features related to a cunique city id
        """
        class_features = db_session.query(base_classes["class_feature"]).filter(
                base_classes["class_feature"].resp_city == city_id
                )
        return class_features
    return get_class_features
    
    
    
def check_file_exits(file_location):
    """
    Check if file exists on s3
    """
        
    client = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=S3_session_token)
    bucket_name = get_bucket(client,)
    client.head_object(Bucket='bucket_name', Key='file_path')
    