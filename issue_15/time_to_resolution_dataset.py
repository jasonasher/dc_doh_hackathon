#!/usr/bin/env python27
# -*- coding: utf-8 -*-

"""
DC311calls_censusBlock_merge.py
DC Health & Human Services Hackathon, September 2017
S.Sylvester: ssylvest00@gmail.com

Extract Time-to-Resolution features from 311 Data #15

The purpose of this script is to combine two datasets
(All_311_Service_Resquests and tl_2016_11_tabblock10.shp) and
compute the average number of days elapsed between features
SERVICEORDERDATE and RESOLUTIONDATE per service code, per week,
and per census block. The final product is a CSV file that
contains this information.
"""

# Import modules
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

# Load data 311 data
dirStr = 'datasets/311_service_requests/OCTO Warehouse/'
fileName = 'All_311_Service_Requests.csv'
dc311_df = pd.read_csv(dirStr + fileName,low_memory = False)

# Load census shape file
dirStr = 'datasets/shapefiles_and_geospatial_information/dc_2010_block_shapefiles/'
fileName = 'tl_2016_11_tabblock10.shp'
census_df = gpd.GeoDataFrame.from_file(dirStr + fileName)

# Remove rows where RESOLUTIONDATE are empty
dc311_df_new = dc311_df[dc311_df['RESOLUTIONDATE'].notnull()].reset_index(drop = True)

# Convert lat/long to geo-object points, make geodataframe of these points
# Inspired by: https://gis.stackexchange.com/questions/174936/geopandas-error-minimums-more-than-maximums
pointList = [Point(xy) for xy in zip(dc311_df_new['LONGITUDE'],dc311_df_new['LATITUDE'])]
df_temp = pd.DataFrame(data = pointList)
df_temp.columns = ['geometry']
geoPoint_df = gpd.GeoDataFrame(df_temp, crs = census_df.crs, geometry = 'geometry')

# Merge census and 311 call data sets
df_merged = gpd.tools.sjoin(geoPoint_df, census_df, how='left')

# Add census block data to 311 service data
df = dc311_df_new
df['census_block_2010'] = df_merged['BLOCKCE10']

# Convert time to datetime object
df['RESOLUTIONDATE'] = pd.to_datetime(df['RESOLUTIONDATE'])
df['SERVICEORDERDATE'] = pd.to_datetime(df['SERVICEORDERDATE'])

# Compute the elapsed time between service order date and resolution date
df['days_to_resolution'] = df['RESOLUTIONDATE'] - df['SERVICEORDERDATE']

# Convert parital datetime object (in hours & minutes) to a fraction of a day
temp_df = df['days_to_resolution'].apply(lambda x: round(x / np.timedelta64(1, 'h')) % 24 )
day_adjustment = temp_df / 24.0

# Add partial day/ fraction to complete day
df['days_to_resolution_adj'] = df['days_to_resolution'].astype('timedelta64[D]') + day_adjustment

# Extract week and year, place in new columns
df['week'] = df['SERVICEORDERDATE'].apply(lambda x: x.week)
df['year'] = df['SERVICEORDERDATE'].apply(lambda x: x.year)

# Groupby week, census block, & service code
# Compute the mean per service code, per week, and per block
temp_df = df.groupby(['SERVICECODE','week','census_block_2010']).mean().reset_index()

# Trim new dataframe
colNames = ['SERVICECODE','year','week','census_block_2010','days_to_resolution_adj']
temp_df = temp_df[colNames]

# Add feature_id and feature_subtype columns
temp_df['feature_id'] = '311_service_requests_ttr'
temp_df['feature_subtype'] = 'NA'

# Rename columns to suit data scheme
temp_df.columns = ['feature_type','year','week','census_block_2010','value','feature_id','feature_subtype']

# Reorder dataframe columns
colNames = ['feature_id','feature_type','feature_subtype','year','week','census_block_2010','value']
temp_df = temp_df[colNames]

# Save dataframe as CSV, remove dataframe index
temp_df.to_csv('time_to_resolution_dataset.csv', index = False)