###############################################################################
# Title: Extract 'Overdue Inspections' Feature from Restaurant Inspection Data #17
# Author: Kathy Xiong
# Last updated: 2017-12-21
#
# Purpose:
# This script summarises the number of overdue restaurant inspections by 
# establishment type and risk category, for each year, week, and census block
# 
# Instructions:
# Update all directory paths to match local file structure before running script
# 
# Inputs:
# - cleaned restaurant inspections and geocoding files:
#   - dc_restaurant_inspections/potential_inspection_summary_data.csv
#   - dc_restaurant_inspections/inspections_geocoded.csv
# - 2010 census blocks shapefile:
#   - census_2010/tl_2016_11_tabblock10.shp, etc.
#
# Outputs:
# - CSV file with overdue inspection values:
#   - restaurant_inspections_overdue.csv
# - Quick visualisation of total inspections by week by risk category:
#   - restaurant_inspections_overdue.png
#
# Open issues:
# - Update inspection frequency requirements with official DOH values
# - Based on inspection frequency requirements, update the earliest date in the
#   output file so that we don't "undercount" overdue inspections in weeks
#   where we don't have enough historical data. For example, if an establishment
#   needs to be inspected every year, and we only have inspection data starting 
#   2008-01-01, we do not know if inspections have occured before 2008-01-01, so
#   we cannot know if it is overdue for inspection until 2009-01-01
###############################################################################

# Set up -----------------------------------------------------------------------
library(tidyverse)
library(lubridate)
library(stringr)
library(ISOweek)
library(rgdal)

setwd("/Users/kathy/Documents/_projects/dc_doh_hackathon")

# Read in data -----------------------------------------------------------------
inspection_geocode <- read_csv("data/dc_restaurant_inspections/inspections_geocoded.csv")
inspection_summary <- read_csv("data/dc_restaurant_inspections/potential_inspection_summary_data.csv")

census_blocks <- readOGR("data/census_2010", "tl_2016_11_tabblock10")

# Create weekly time intervals to loop over ------------------------------------

## Dataset appears to contain inspections between 2008-01-08 and 2017-09-11. 
## So we will use that as the start and end dates.
## See explore_restaurant_inspections.Rmd for details.
##
## Also we will use Monday of each week as the cutoff to calculate # of
## overdue inspections.

first_day <- date2ISOweek("2008-01-08")
first_monday <- paste0(str_sub(first_day, 1, -2), "1")
first_monday <- ISOweek2date(first_monday)

last_day <- date2ISOweek("2017-09-11")
last_monday <- paste0(str_sub(last_day, 1, -2), "1")
last_monday <- ISOweek2date(last_monday)

mondays <- seq(first_monday, last_monday, by = 7)

# Prepare inspections data -----------------------------------------------------
# Add required inspection frequencies. 
## These are PLACEHOLDERS ONLY. To be updated with real frequencies from DOH.
## For reasoning behind these guesses, see explore_restaurant_inspections.Rmd
inspection_summary_1 <- inspection_summary %>% 
  mutate(
    inspection_frequency = case_when(
      risk_category == 1 ~ 900,
      risk_category == 2 ~ 600,
      risk_category == 3 ~ 600,
      risk_category == 4 ~ 600,
      risk_category == 5 ~ 600
    )
  )

## Turn inspection geocodes into a spatial object
## Note that the coordinates are taken from ggmap (see issue #13 submission) 
## which uses the WGS84 datum. For reference see p2, "3. Add polygons from sp file",
## https://www.nceas.ucsb.edu/~frazier/RSpatialGuides/ggmap/ggmapCheatsheet.pdf

inspection_coord <- inspection_geocode %>% 
  select(longitude, latitude)

inspection_spdf <- SpatialPointsDataFrame(coords = inspection_coord, 
                                          data = inspection_geocode,
                                          proj4string = CRS("+proj=longlat +datum=WGS84"))

# Project census blocks shapefile
census_blocks_projected <- spTransform(census_blocks, inspection_spdf@proj4string)

# Determine census block for each inspection
inspection_block <- over(inspection_spdf, census_blocks_projected)
inspection_spdf$census_block_2010 <- inspection_block$BLOCKCE10

# Add census block to summary dataset
inspection_summary_2 <- inspection_summary_1 %>% 
  left_join(inspection_spdf@data, by = "inspection_id")

# Extract overdue inspections --------------------------------------------------
# Create loop to extract overdue inspections in any given week
res <- vector("list", length(mondays))

for (i in seq_along(mondays)) {
  
  # Get the most recent (prior to start of week) inspection per establishment
  data <- inspection_summary_2 %>% 
    filter(inspection_date <= mondays[i]) %>% 
    arrange(establishment_name, address, desc(inspection_date)) %>% 
    group_by(establishment_name, address) %>% 
    filter(row_number() == 1)
  
  data <- data %>% 
    mutate(current_date = mondays[i],
           days_since_last_inspection = current_date - inspection_date,
           overdue = (days_since_last_inspection > inspection_frequency)
    )
  
  res[[i]] <- data %>% 
    group_by(current_date, establishment_type, risk_category, census_block_2010) %>% 
    summarise(value = sum(overdue))
  
}

res_1 <- bind_rows(res)
res_2 <- res_1 %>% 
  ungroup() %>% 
  mutate(feature_id = "restaurant_inspections_overdue",
         feature_type = establishment_type,
         feature_subtype = risk_category,
         year = year(current_date),
         week = isoweek(current_date)) %>% 
  select(feature_id,
         feature_type,
         feature_subtype,
         year,
         week,
         census_block_2010,
         value)

write_csv(res_2, "issue_17/restaurant_inspections_overdue.csv")

# visualize
res_1 %>% 
  ungroup() %>% 
  group_by(risk_category, current_date) %>% 
  summarise(total_overdue = sum(value)) %>% 
  ggplot() +
  geom_bar(aes(x = current_date, y = total_overdue), stat = "identity") +
  facet_wrap(~risk_category)

ggsave("issue_17/restaurant_inspections_overdue.png")
