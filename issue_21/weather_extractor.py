
# coding: utf-8

# In[33]:


import pandas as pd
import os
import datetime


# In[34]:


def get_iso_date(date_str):
    #Input: string of format 'yyyy-mm-dd'
    
    #Output: 3-tuple of format (ISO year, ISO week number, ISO weekday)    
    
    year = int(date_str[:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    return(datetime.date(year, month, day).isocalendar())


# In[35]:


def main(input_dir, output_dir):
    # Input: A directory containing weather data organized from oldest to newest
    
    # Output: A feature data table -- including total precipitation, average temperature,
    #         average maximum temperature, and average minimum temperature -- aggregated by week.

    #### read in files from directory and concatenate into one data frame ####
    
    file_list = []
    for filename in os.listdir(input_dir):
        file_list.append(pd.read_csv(os.path.join(input_dir, filename)))
    df_total = pd.concat(file_list)
    
    # create an empty final feature table
    df_aggregated = pd.DataFrame(columns = ['feature_id', 'feature_type', 'feature_subtype',
                                        'year', 'week', 'census_block_2010', 'value'])

    ##########################################################################
    

    ########## find first monday of the year to avoid partial week ##########

    # check the week number of the 7th day; this will always be a full week
    week_of_day_7 = get_iso_date(df_total.iloc[6, 1])[1]
    
    # find the first day in that same week number; this is first Monday 
    first_monday_idx = 0
    date_str = df_total.iloc[0, 1]
    while(get_iso_date(date_str)[1] != week_of_day_7):
        first_monday_idx += 1
        date_str = df_total.iloc[first_monday_idx, 1]
    
    ##########################################################################
    
    
    ################### iterate over data set by week ########################

    for i in range(first_monday_idx, df_total.shape[0], 7):
        temp_vals = {}
        iso_date = get_iso_date(df_total.iloc[i, 1])

        # add each of the four different features for this week

        # Total precipitation
        df_aggregated = df_aggregated.append({'feature_id' : 'weather_total_precipitation', 'value': df_total.iloc[i:i+7, 2].sum(axis=0),
                                                'year': iso_date[0], 'week' : iso_date[1]}, ignore_index=True)
        # Weather Average Temperature
        df_aggregated = df_aggregated.append({'feature_id' : 'weather_average_temperature', 'value': df_total.iloc[i:i+7, 5].mean(axis=0),
                                                'year': iso_date[0], 'week' : iso_date[1]}, ignore_index=True)

        # Weather Average Minimum Temperatue
        df_aggregated = df_aggregated.append({'feature_id' : 'weather_average_minimum_temperature', 'value': df_total.iloc[i:i+7, 7].mean(axis=0),
                                                'year': iso_date[0], 'week' : iso_date[1]}, ignore_index=True)
        # Weather Average Maximum Temperature
        df_aggregated = df_aggregated.append({'feature_id' : 'weather_average_maximum_temperature', 'value': df_total.iloc[i:i+7, 6].mean(axis=0),
                                                'year': iso_date[0], 'week' : iso_date[1]}, ignore_index=True)
    
    #######################################################################
    

    # output to csv
    df_aggregated.to_csv('weather_at_national_airport.csv')


# In[36]:


input_dir = './/airport_weather_data_raw'
output_dir = './/'
main(input_dir, output_dir)

