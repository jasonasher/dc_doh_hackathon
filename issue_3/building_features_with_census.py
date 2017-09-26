#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import geopandas
import geopandas.tools
from shapely.geometry import Point
 
# Note: you will need to install the rtree package - http://toblerity.org/rtree/install.html
 
#read in data
fields=['ISSUE_DATE', 'PERMIT_TYPE_NAME', 'PERMIT_SUBTYPE_NAME', 'LONGITUDE', 'LATITUDE']
df = pd.read_csv('All_Building_permits.csv', usecols=fields)

#geocode lat long to census block
df['geometry'] = df.apply(lambda row: Point(row['LONGITUDE'], row['LATITUDE']), axis=1)
df = geopandas.GeoDataFrame(df, geometry='geometry')
df.crs = {'init': 'epsg:4326'}
 
census_blocks = geopandas.GeoDataFrame.from_file('dc_2010_block_shapefiles/tl_2016_11_tabblock10.shp')
census_blocks.crs = {'init': 'epsg:4326'}
 
result = geopandas.tools.sjoin(df[['geometry']], census_blocks[['BLOCKCE10', 'geometry']], how='left')
 
df['census_block_2010'] = result['BLOCKCE10']
df = df[fields + ['census_block_2010']]

#clean up, rename
del df['LONGITUDE']
del df['LATITUDE']
df = df.rename(columns={'PERMIT_TYPE_NAME': 'feature_type', 'PERMIT_SUBTYPE_NAME':'feature_subtype'})

#convert date column to date type 
df['ISSUE_DATE'] = pd.to_datetime(df.ISSUE_DATE)

#grab the last four weeks (28 days) of data from the last data point, 9/20/2017
lastdayfrom = pd.to_datetime('9/20/2017')
df = df.set_index('ISSUE_DATE')
df.index = df.index.sort_values()
df = df.loc[lastdayfrom - pd.Timedelta(days=28):lastdayfrom].reset_index()

#break ISSUE_DATE into year and week fields 
df['year'], df['week'] = df['ISSUE_DATE'].dt.year, df['ISSUE_DATE'].dt.week
del df['ISSUE_DATE']

#adding value and feature_id field
df = df.groupby(['feature_type', 'feature_subtype', 'census_block_2010', 'year', 'week']).size()
df = df.reset_index()
df = df.rename(columns={0:'value'})
df['feature_id'] = 'building_permits_issued_last_4_weeks'

#take a look
print(df)
