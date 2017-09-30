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
  
  data_with_census <- data %>%
    mutate(XXXrow_number = row_numbers) %>%
    left_join(data_spatial@data %>%
                cbind(data_spatial_block) %>%
                dplyr::select(row_number, BLOCKCE10) %>%
                dplyr::rename(census_block = BLOCKCE10),
              by = c("XXXrow_number" = "row_number")) %>%
    dplyr::select(-XXXrow_number)
}

