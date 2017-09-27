# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 11:14:37 2017

@author: Andrew Rawlings
"""
# Import libraries
import pandas as pd
import os
import geopandas
import shapely


# Functions
def calcPercentage(block):
    ANCIntersection = []
    for index, row in anc2013.iterrows():
        ANCIntersection.append((row['NAME'],block.intersection(row['geometry']).area))
    df = pd.DataFrame(ANCIntersection,columns=['NAME','INTERSECTION_AREA'])
    totalArea = sum(df['INTERSECTION_AREA'])
    df['Percentage']= df['INTERSECTION_AREA']/totalArea
    return df

# Return max percentage ANC and the name of the respective ANC
def calcMaxPercentage(block):
    ANCIntersection = []
    for index, row in anc2013.iterrows():
        ANCIntersection.append((row['ANC_ID'],block.intersection(row['geometry']).area))
    df = pd.DataFrame(ANCIntersection,columns=['ANC_ID','INTERSECTION_AREA'])
    totalArea = sum(df['INTERSECTION_AREA'])
    df['Percentage']= df['INTERSECTION_AREA']/totalArea
    maxPercentage = df.loc[df['Percentage'].idxmax()]
    return (maxPercentage['ANC_ID'],maxPercentage['Percentage'],maxPercentage['ANC_ID'][0])

# Read shapefiles with Geopandas
# change path for shape files as appopriate
os.chdir('E:\\VM\DOHHackathon\\Data Sets\\shapefiles and geospatial information\\dc_2010_block_shapefiles')
block2010=geopandas.read_file('tl_2016_11_tabblock10.shp')



# change path for shape files as appopriate
os.chdir('E:\\VM\DOHHackathon\\Data Sets\\shapefiles and geospatial information\\dc_2013_anc_shapefiles')
anc2013 = geopandas.read_file('Advisory_Neighborhood_Commissions_from_2013.shp')

# Cast coordinate system to same as ANC 2013
block2010New=block2010.to_crs(anc2013.crs)

# Apply functions to get block group and census tract , and census block
block2010New['BLOCKGROUP']=block2010New['GEOID10'].apply(lambda x : x[0:12])
block2010New['CENSUSTRACT']=block2010New['GEOID10'].apply(lambda x : x[5:9])
block2010New['CENSUSBLOCK']=block2010New['GEOID10'].apply(lambda x: x[-4:])


# Join with Geopandas,most of these blocks are fully within a single ANC ( the happy path)
block_anc = geopandas.sjoin(block2010New,anc2013, how="left", op='within')


# For those that aren't fully in a single ANC, take the ANC that overlaps the most with the block
block2010New['PercAndArea']=block2010New['geometry'].apply(calcMaxPercentage)
block2010New['blockMaxPercArea']=block2010New['PercAndArea'].apply(lambda x: x[1])
block2010New['BlockANCName']=block2010New['PercAndArea'].apply(lambda x: x[0])
block2010New['BlockWard']=block2010New['PercAndArea'].apply(lambda x: x[2])

# Create output dataset
output= block2010New[['GEOID10','CENSUSTRACT','CENSUSBLOCK','BlockWard','BlockANCName']]
output.columns=['fips15','census_tract','census_block','ward_2010','anc_2010']

# Output to CSV file  in current path, change as appropriate
os.chdir('E:\\VM\\DOHHackathon')
output.to_csv('SpatialCrossWalkOutput.csv',index=False)






    
