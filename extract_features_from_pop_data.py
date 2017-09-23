
# coding: utf-8

# In[12]:

import pandas as pd
import numpy as np
import os


# In[36]:

def main(input_dir, output_dir):
    """
    Reads all files in input_dir, assuming those files contain population by census block data,
    and extracts features.
    
    Saves a "population by block group" csv and a "population by tract" csv.
    """
    # Read all files in input_dir and concatenate
    # This creates dataframe w/ population by block group, "bg_pop"
    file_list = []
    for filename in os.listdir(path):
        bg_pop = pd.read_csv(os.path.join(path, filename))
        file_list.append(bg_pop)
    bg_pop = pd.concat(file_list)

    # Extract census tract variable and put bg_pop in requested format
    bg_pop['GEOID'] = bg_pop.GEOID.astype(str)
    bg_pop['census_tract_2010'] = bg_pop.GEOID.str.extract('(.{11})', expand=False)
    bg_pop['feature_id'] = 'population'
    bg_pop['feature_type'] = np.nan
    bg_pop['feature_subtype'] = np.nan
    bg_pop['week'] = np.nan
    bg_pop.columns = ['census_block_group_2010', 'NAME', 'value', 'year', 'census_tract_2010', 'feature_id', 
                      'feature_type', 'feature_subtype', 'week']
    bg_pop = bg_pop[['feature_id', 'feature_type', 'feature_subtype', 'year', 'week', 'census_block_group_2010', 
            'census_tract_2010', 'value']]

    # Create dataframe w/ population by tract, "tract_pop"
    # Put tract_pop in requested format
    tract_pop = bg_pop.groupby(['year', 'census_tract_2010']).value.sum().reset_index()
    tract_pop['feature_id'] = 'population'
    tract_pop['feature_type'] = np.nan
    tract_pop['feature_subtype'] = np.nan
    tract_pop['week'] = np.nan
    tract_pop = tract_pop[['feature_id', 'feature_type', 'feature_subtype', 'year', 'week', 'census_tract_2010', 
                           'value']]
    
    # Remove tract variable from bg_pop
    bg_pop.drop('census_tract_2010', axis=1, inplace=True)
    
    # Save data to output_dir
    bg_pop.to_csv(os.path.join(output_dir, 'census_block_group_pop.csv'))
    tract_pop.to_csv(os.path.join(output_dir, 'census_tract_pop.csv'))
    
    


# In[37]:

input_dir = '/Users/zeromh/ds/datakind/dc_doh_hackathon/data/Population by Census Block/2013-2015 Population by Census Block Data'
output_dir = '/Users/zeromh/ds/datakind/dc_doh_hackathon/data/Population by Census Block'

main(input_dir, output_dir)

