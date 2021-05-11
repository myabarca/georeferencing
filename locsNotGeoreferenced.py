# -*- coding: utf-8 -*-
"""
Created on Mon May  3 13:56:32 2021

@author: abarc
"""

import pandas as pd

locality = pd.read_csv('C:/Users/abarc/CASG_LocalityDB_downloadedMay032021.csv')

georef = pd.read_csv('C:/Users/abarc/allGeoreferencedToBeImported_downloadedMay032021.csv')

## isin wasn't working when comparing locationID columns. I think it's because of the decimals
## and alphanumerics messing up the datatypes (tried to change datatypes and that also
## didn't help. 
## so going to delete the alphanumerics and see if that helps

#dropping na's and alphanumerics
locality.dropna(how='all', inplace = True)
alphanumeric_indexes = [*range(8503, 8563, 1)]
locality.drop(alphanumeric_indexes, inplace = True)
georef.drop([1110,1111,1112], inplace=True)

## check dtypes for locationID
locality.info()
georef.info()
## both objects, but the decimals in locality locationIDs are gone

# make list of georeferenced localities to compare to locality locationIDs
georefLocIDS = georef['locationID'].to_list()
print (georefLocIDS)
## PROBLEM IS THAT THE LIST VALUES ARE STRINGS. CHANGE TO INT
georefLocIDS = list(map(int, georefLocIDS))

# using query method works 
query_test = locality.query("locationID not in @georefLocIDS")

# using ~isin also works and gives same df as query method 
is_in_test = locality[~locality['locationID'].isin(georefLocIDS)]

#not sure why merge returns empty df 
merged = locality.merge(georef, how='inner', on='locationID')

query_test.to_csv('casgLocsNotYetGeoreferenced_May042021.csv', index=False)









