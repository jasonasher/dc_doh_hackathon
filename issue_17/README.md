# Issue #17 Extract 'Overdue Inspections' Feature from Restaurant Inspection Data

This script summarizes the restaurant inspections data by year, week, census block,
establishment type, and risk category, and creates two features: number of overdue inspections and average number of days since last inspection (inspection frequency). The second output is not part of the original issue and is added as an alternative feature to test.

## Instructions

Update directory paths in section labeled "UPDATE PATHS" before running script

## Inputs

Cleaned restaurant inspections and geocoding files:
* dc_restaurant_inspections/potential_inspection_summary_data.csv
* dc_restaurant_inspections/restaurant_inspections_geocoded.csv

## Outputs

CSV files with features:
* restaurant_inspections_overdue.csv
* restaurant_inspections_frequency.csv

Quick visualisations by week by risk category:
* restaurant_inspections_overdue.png
* restaurant_inspections_frequency.png

## Open issues

* Update inspection frequency requirements with official DOH values
* Decide what to do about the 'bias' towards fewer overdue inspections & more frequent inspections in earlier time periods. In the earlier time periods, most establishment would have an "NA" for days since last inspection, because their last inspection is not in the data set; only those that have had inspections very recently (i.e. since start of data set) would have a value and be included in the aggregate calculations.
