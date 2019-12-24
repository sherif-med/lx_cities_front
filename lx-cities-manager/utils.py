#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 14:51:24 2019

@author: cherif
"""

import fiona
from decouple import config
import boto3
from botocore.errorfactory import ClientError
from session import db_session, base_classes
from urllib.parse import urlparse
# ParseResult(scheme='s3', netloc='bucket_name', path='/folder1/folder2/file1.json', params='', query='', fragment='')
import rasterio

aws_access_key_id = config('AWS_ACCESS_KEY_ID')
aws_secret_access_key = config('AWS_SECRET_ACCESS_KEY')
S3_session_token = config('S3_SESSION_TOKEN')

def get_boto3_session():
    
    sess = boto3.session.Session(aws_access_key_id = aws_access_key_id,
                     aws_secret_access_key = aws_secret_access_key,
                     aws_session_token=S3_session_token)
    return sess

def get_raster_from_s3(file_location):
    """
    Loads tiff file from s3.
    Args:
        file_location : example: s3://bucket/file.tif
    Returns:
        
    """
    rasterio_obj = []
    boto3_session = get_boto3_session()
    with rasterio.Env(rasterio.session.AWSSession(boto3_session)):
        print (f"Loading file {file_location}")
        rasterio_obj = rasterio.open(file_location)
    return rasterio_obj

def get_shape_from_s3(file_location):
    """
    Loads esri shape file from s3.
    Args:
        file_location : example: s3://bucket/file.shp
    Returns:
        fiona_collection : fiona object conatining features
    """
    fiona_collection = []
    boto3_session = get_boto3_session()
    with fiona.Env(session = fiona.session.AWSSession(boto3_session)):
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
                ).all()
        return class_features
    return get_class_features(city_id)
    
    
    
def check_file_exits(file_location):
    """
    Check if file exists on s3
    """
        
    client = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=S3_session_token)
    parsed = urlparse(file_location, allow_fragments=False)
    bucket_name, key = parsed.netloc, parsed.path
    result = client.list_objects(Bucket=bucket_name, Prefix=key)
    
    return 'Contents' in result
 

from functools import partial
import pyproj
from shapely.ops import transform

def reproject_geom(geom, epsg_code, epsg_code_init='epsg:4326'):
    project = partial(
        pyproj.transform,
        pyproj.Proj(init=epsg_code_init.lower()), # source coordinate system
        pyproj.Proj(init=epsg_code.lower())
        )
    projected_geom = transform(project, geom)
    return projected_geom

