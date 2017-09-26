library(lubridate)
library(dplyr)

setwd('C:/Users/xavie/Desktop/dc_doh_hackathon') # When this file is sourced it captures the current directory

inspections <- read_csv("Restaurant Inspections/potential_inspection_summary_data.csv")
location <- read_csv("restaurants/inspection_geocodes_w_block.csv") # created using add_census_block_data.R from DropBox

# add new cols
inspections$census_block <- location$census_block
inspections$year <- year(inspections$inspection_date)
inspections$week <- week(inspections$inspection_date)

# process inspection_type string
inspections$inspection_type <- tolower(inspections$inspection_type)


# filter and count
data <- inspections %>%
    select(establishment_type, risk_category, year, week, census_block, inspection_type) %>%
    filter(inspection_type == 'complaint') %>%
    group_by(establishment_type, risk_category, year, week, census_block) %>%
    summarise(value=n()) %>%
    mutate(restaurant_inspection_complaints = 'restaurant_inspection_complaints') %>%
    arrange(restaurant_inspection_complaints, establishment_type, risk_category, year, week, census_block, value)

write_csv(data, "restaurants/new complaints.csv")
