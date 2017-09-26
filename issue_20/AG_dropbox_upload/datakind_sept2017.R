# DC Data Kind 
# Analyst - Anirban Ghosh 
# Used R
# Filtered out all "known_valid != True"


# Aim - 
#   Create a dataset with one row per:
#   1. establishment type
#   2. risk category, 
#   3. each week, 
#   4. year, 
#   5. census block


# We need the following features in the dataset
# feature_id: The ID for the feature, in this case, "food_service_establishments" <- generate 
# feature_type: The establishment_type from the restaurant data set
# feature_subtype: The risk_category from 1-5
# year: The ISO-8601 year of the feature value
# week: The ISO-8601 week number of the feature value
# census_block_2010: The 2010 Census Block of the feature value
# value: The value of the feature, i.e. 
#       the number of food service establishments with the given 
#       types and risk categories in the specified week, year, and census block.

setwd("C://Users//aghosh//Desktop//Temp//2017 09 DataKindDC//Restaurant Inspections//Scraped Restaurant Inspection Data To Be Validated")

library(tidyverse)
df <- read.csv("potential_inspection_summary_data.csv")

# Reviewing the data.

str(df)
names(df)
head(df, 10)

class(dfinspection_date)
# This is a factor.  Should recode as date.  
# variables of interest:
#   1. establishment_type
#   2. risk_category
#   3. inspection_date - use to generate week and year 
# 
# sum the number of establishments 
# 
# Not in this data - the census block. Need to merge in geocode information 

nrow(distinct(df))
# Looks like one duplicate

df1 <- df %>% unique()
# Dropped one observation 

df1$inspect_date <- parse_date(as.character(df1$inspection_date))

library(lubridate)
df2 <- df1 %>% 
mutate(
  week = week(inspect_date), 
  year = year(inspect_date)
) 


# Getting the lat long data  ----------------------------------------------
setwd("C://Users//aghosh//Desktop//Temp//2017 09 DataKindDC//Restaurant Inspections//Updated Geocodes")
latlong <- read.csv("inspection_geocodes.csv")

View(latlong)
 
df3<- inner_join(latlong, df2, by = "inspection_id")
# there is a one to one join between latlong and the cleaned dataset. 


# Load Census Tract -------------------------------------------------------

#https://stackoverflow.com/questions/29872109/binning-longitude-latitude-labeled-data-by-census-block-id

install.packages('rgdal',dependencies=TRUE, repos='http://cran.rstudio.com/') 
install.packages('raster',dependencies=TRUE, repos='http://cran.rstudio.com/') 

library(rgdal)
library(sp)
library(raster)
library(readr)
library(dplyr)

#####
# Compute polygon intersection locally using census block shapefiles
# Returns the same data frame with an additional column at the end called 'census_block'
#
add_census_block_data <- function(data, lat_col_name = "latitude", lon_col_name = "longitude") {
  
  census_block_data <- shapefile("dc_2010_block_shapefiles/tl_2016_11_tabblock10.shp")
  census_block_data <- spTransform(census_block_data, CRSobj=CRS("+proj=longlat +datum=WGS84"))
  
  row_numbers <- 1:nrow(data) # used as a unique id
  
  data_spatial <- SpatialPointsDataFrame(coords = data[, c(lon_col_name, lat_col_name)],
                                         data = data_frame(row_number = row_numbers),
                                         proj4string=CRS("+proj=longlat +datum=WGS84"))
  
  data_spatial_block <- over(x = data_spatial, y = census_block_data)
}

blocks <- add_census_block_data(df3, "latitude", "longitude")
blocks1 <- blocks  
blocks1$row_numbers <- 1:nrow(blocks1)
df4 <- df3
df4$row_numbers <- 1:nrow(df4)
# Note that i merged by row number, which is not ideal but I 
# cannot find a better way to merge by lat and long.  

df5 <- inner_join(df4, blocks1, by = "row_numbers")

df6 <- df5 %>% 
  mutate(
    known_valid = as.character(known_valid),
    feature_id = "food_service_establishments" 
  ) %>% 
  filter(
    known_valid == "True"
  )


 
# df6 has all the data i need  --------------------------------------------

final <- df6 %>% 
  group_by(
    establishment_type,
    risk_category, 
    week,
    year, 
    BLOCKCE10,
    feature_id
  ) %>% 
  summarise(
    value = n()
  ) %>% 
  rename(
    feature_type = establishment_type, 
    feature_subtype = risk_category, 
    census_block_2010 = BLOCKCE10
  )

write_rds(final, "Number_of_Establishments.rds")
write_csv(final, "Number_of_Establishments.csv")

# End of Issue 20  --------------------------------------------------------


