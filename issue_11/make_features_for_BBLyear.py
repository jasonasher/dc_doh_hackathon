import pandas as pd
import datetime

# change below for the different csv files; could use sys.argv
fName = 'Basic_Business_License_in_2015.csv'
outName = fName.replace('.csv', '-features.csv')

df = pd.read_csv(fName)

# clean up missing data by dropping rows
invalIx = df.LICENSE_EXPIRATION_DATE.apply(lambda x: type(x)!=str)
df = df.loc[~invalIx,:]

# parse the datestrings into useful columns
df['expDatetime'] = df.LICENSE_EXPIRATION_DATE.\
                    apply(lambda x: pd.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000Z'))
df['expYear'] = df.expDatetime.apply(lambda x: int(x.strftime('%Y')))
df['expWeek'] = df.expDatetime.apply(lambda x: int(x.strftime('%U')))

df['issueDatetime'] = df.LICENSE_ISSUE_DATE.\
                      apply(lambda x: pd.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000Z'))
df['issueYear'] = df.issueDatetime.apply(lambda x: int(x.strftime('%Y')))
df['issueWeek'] = df.issueDatetime.apply(lambda x: int(x.strftime('%U')))

################
# add code here to convert lat/long into census block numbers

# should look something like this
#df['census_block_2010'] = df[['LATITUDE','LONGITUDE']].\
#    apply(lambda x: fancy_geopandas_function(x[0],x[1]))

# in the meantime - generate dummy locs from math on lat/long.  149 unique locs in 2015
df['census_block_2010'] = np.floor(df.LATITUDE*df.LONGITUDE*10)
################

# extract unique values of columns to iterate over
all_types = np.unique(df.LICENSECATEGORY)
all_blocks = np.unique(df.census_block_2010)
all_years = np.unique(df.issueYear)

# subset by licensecategory for speed
dfD = {}
for tT in all_types:
    dfD[tT] = df.loc[df.LICENSECATEGORY == tT,:]



# 1st output df: in effect
# iterate over year, week, types, census blocks; calculate value, make a list of dicts for convert to dataframe
print('Doing licenses_in_effect: rows: ', end='')
dictL = []

for (iY,tY) in enumerate(all_years):  # a bit hacky to iterate over years and weeks; should iterate over week,year pairs fm 1st to last in file
    for (iW,tW) in enumerate(range(52)):
        for (iC,tC) in enumerate(all_types):
            df0 = dfD[tC] # split by category
            tDatetime = datetime.datetime.strptime('%d-%02d-Sun'%(tY,tW), '%Y-%U-%a')  # need to add weekday for %U to work, see py docs

            issuedByNowIx = df0.issueDatetime <= tDatetime
            expiredByNowIx = df0.expDatetime >= tDatetime
            
            desIx = (issuedByNowIx & ~expiredByNowIx)
            
            # now iterate only over the census blocks found to have records - might be a bit of premature
            # opt, but probably saves some time b/c a quick profile shows sum(desIx) is often zero
            cbV = df0.census_block_2010[desIx]
            cbL = np.unique(cbV)
            for (iB,tB) in enumerate(cbL):
                tV = np.sum(cbV==tB)
            
                # create the new row
                dictL.append({'feature_id': 'business_licenses_in_effect', 
                                'feature_type': tC, 
                                'year': tY, 'week': tW, 
                                'census_block_2010': tB,
                                'value': tV})
        print(len(dictL), end=', ')  # print update after each week
newdf1 = pd.DataFrame(dictL)

# 2nd dataframe with business_licenses_issued_last_4_weeks
print('Doing rows: ', end='')
dictL = []
for (iY,tY) in enumerate(all_years):
    for (iW,tW) in enumerate(range(52)):
        for (iC,tC) in enumerate(all_types):
            df0 = dfD[tC] # split by category
            endDt = datetime.datetime.strptime('%d-%02d-Sun'%(tY,tW), '%Y-%U-%a')  # need to add weekday for %U to work, see py docs
            beginDt = endDt - datetime.timedelta(days=28)
            
            issuedByNowIx = df0.issueDatetime <= tDatetime
            expiredByNowIx = df0.expDatetime >= tDatetime
            desIx = (df0.issueDatetime >= beginDt) & (df0.issueDatetime <= endDt)
            
            # now iterate only over the census blocks found to have records - might be a bit of premature
            # opt, but probably saves some time b/c a quick profile shows sum(desIx) is often zero
            cbV = df0.census_block_2010[desIx]
            cbL = np.unique(cbV)
            for (iB,tB) in enumerate(cbL):
                tV = np.sum(cbV==tB)
            
                # create the new row
                dictL.append({'feature_id': 'business_licenses_issued_last_4_weeks',
                                'feature_type': tC, 
                                'year': tY, 'week': tW, 
                                'census_block_2010': tB,
                                'value': tV})
        print(len(dictL), end=', ')  # print update after each week
newdf2 = pd.DataFrame(dictL)

# write output csv
fulloutdf = pd.concat([newdf1,newdf2])
fulloutdf.to_csv(outName, index=False)
