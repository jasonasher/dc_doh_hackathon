
# coding: utf-8

# In[ ]:


#A script to close issue #20 @https://github.com/jasonasher/dc_doh_hackathon
#By Charles Landau
#Email CharlesDLandau@gmail.com


# In[2]:


import pandas as pd
import numpy as np
import geopandas as gpd


# In[3]:


import SALib as sa
import requests
import statsmodels as stk
import sklearn as sm
from shapely.geometry import Point


# # DC HHS Hackathon

# In[30]:


def pull_inspections(colToCount):
    #A value which returns the "long multindexed" value counts of a user-defined STRING column name.
    #User needs potential_inspection_summary_data.csv
    #User needs inspections_geocoded.csv
    #User needs dc_2010_block_shapefiles file from the team dropbox
    insp_sum = pd.read_csv('./data/potential_inspection_summary_data.csv')
    insp_vio = pd.read_csv('./data/potential_violation_details_data.csv')
    insp_geo = pd.read_csv('./data/inspections_geocoded.csv')
    

    insp_sum = pd.merge(insp_sum, insp_geo, on='inspection_id', how='inner')

    insp_sum['inspection_date'] = pd.to_datetime(insp_sum['inspection_date'])

    insp_sum.T

    # Note: you will need to install the rtree package - http://toblerity.org/rtree/install.html

    data = insp_sum
    column_names = list(data.columns.values)

    data['geometry'] = data.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
    data1 = data
    data = gpd.GeoDataFrame(data, geometry='geometry')
    data.crs = {'init': 'epsg:4326'}

    census_blocks = gpd.GeoDataFrame.from_file('./data/dc_2010_block_shapefiles/tl_2016_11_tabblock10.shp')
    census_blocks.crs = {'init': 'epsg:4326'}

    result = gpd.tools.sjoin(data, census_blocks[['BLOCKCE10', 'geometry']], how='inner')

    #data['census_block'] = result['BLOCKCE10']

    result

    result.to_csv('./data/data_with_census_block.csv', encoding='utf-8', index=False)

    insp_sum = result

    insp_sum['year'] = insp_sum['inspection_date'].dt.year
    insp_sum['week'] = insp_sum['inspection_date'].dt.week

    head = ['establishment_type', 'risk_category',
            colToCount, 'year', 'week', 'BLOCKCE10']

    cols = ['establishment_type', 'risk_category',
                              'year', 'week', 'BLOCKCE10']

    typify = insp_sum[head]

    typify = typify.groupby(cols)
    typify = pd.DataFrame(typify.count())
    typify.rename(columns= {colToCount : 'values'}, inplace=True)
    typify.to_csv('./data/out.csv')
    typify


# In[31]:





# In[32]:




