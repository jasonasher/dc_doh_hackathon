

library('dplyr')
library('lubridate')
library('readr')
# read in datamake sure that the unzipped Datafilesand the DC_2010_block_shapefiles 
# folders are in your path before running these scripts 
# make sure add_census_block_data.r is sources as well
source('add_census_block_data.R')

I_Geo= read_csv('inspections_geocoded.csv')
Inspect=read_csv('potential_inspection_summary_data.csv')
Violations= read_csv('potential_violation_details_data.csv')



# Convert Violation Data to give one output value for each inspection corresponding to 
# how many rodent or trash violations (violation codes 38 and 54) 
 
  
Rodent_or_trash <- Violations %>% dplyr::select(inspection_id,violation_number) %>%
               transmute( inspection_id = inspection_id,
               Rodent_or_trash = as.integer(Violations$violation_number %in% c(38,54)))%>%
               filter(inspection_id,Rodent_or_trash == 1 ) %>% unique()
             
  


# add census blocks and Rodent or trash to Inspection Data

I_Block <-add_census_block_data(I_Geo)

Inspect <- left_join(Inspect,I_Block,         by ="inspection_id")
Inspect <- left_join(Inspect,Rodent_or_trash, by = "inspection_id")
Inspect[is.na(Inspect$Rodent_or_trash),'Rodent_or_trash'] = 0 
Inspect$inspection_date <- lubridate::ymd(Inspect$inspection_date)

# Change Date to week and year variables and then group variables by 
# census block, establishment type, risk category and Date
out <-Inspect %>% mutate(week = lubridate::week(inspection_date),
                         year = lubridate::year(inspection_date) ) %>% 
                  dplyr::select(census_block,establishment_type,risk_category,
                         Rodent_or_trash,week,year) %>%
                  group_by(census_block,establishment_type,risk_category,
                           week,year)%>%
                  summarise(value = sum(Rodent_or_trash) ) %>% 
       
             mutate(feature_id = 'restaurant_violations_rodent_or_trash')
                   
names(out) <-c('census_block_2010','feature_type','feature_subtype','year','week','value','feature_id')
write_csv(out, file.path(getwd(), 'restaurant_violations_rodent_or_trash_tidy.csv'))



