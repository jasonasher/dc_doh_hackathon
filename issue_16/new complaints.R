require(lubridate)
require(dplyr)
require(readr)

args <- commandArgs(trailingOnly = TRUE)

inspections <- read_csv(args[1])
location <- read_csv(args[2]) # created using add_census_block_data.R from DropBox

# add new cols
inspections$census_block <- location$census_block
inspections$year <- year(inspections$inspection_date)
inspections$week <- week(inspections$inspection_date)

# process inspection_type string
inspections$inspection_type <- tolower(inspections$inspection_type)


# filter and count
data <- inspections %>%
    select(establishment_type, establishment_name, risk_category, year, week, census_block, inspection_type) %>%
    filter(inspection_type == 'complaint') %>%
    group_by(establishment_type, risk_category, year, week, census_block) %>%
    summarise(value=n()) %>%
    mutate(restaurant_inspection_complaints = 'restaurant_inspection_complaints') %>%
    arrange(restaurant_inspection_complaints, establishment_type, risk_category, year, week, census_block, value)

write_csv(data, paste(args[3],".csv", sep = ""))
