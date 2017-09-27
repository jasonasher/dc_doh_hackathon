This code uses the shapefiles that were in the DC hackahton dropbox for census block and ANC.  The paths are the ones I used on the local machine and they will need to be changed as appropriate.

The current iteration of this code matches all the census blocks that are fully contained within a single ANC with that ANC

For the more complicated case of a census block spanning multiple ANCs, the logic in the current code takes the ANC with the largest overlap.
Ex. If a census block is 97% in one ANC and 3% in another, the ANC that matches with the census block for 97% of it's area will be used. 


Another way of doing this would be create a crosswalk with all the possiblities, and it would be fairly easy to adapt the code to do that.

The output is in a CSV file called SpatialCrossWalkOutput.csv