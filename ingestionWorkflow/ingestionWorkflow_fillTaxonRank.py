# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 16:00:55 2022

Updated 26 May 2022
"""

# Filemaker records did not record taxonRank and scientificName fields.
# These fields were included in EPICC data in order to facilitate taxon matching in GBIF.
# This script fills in empty taxonRank and scientficName for Filemaker records (and those EPICC records where it is blank) where genus and species were recorded.
# After this was run, the remaining records with empty taxonRank and scientificName were manually reviewed and filled in.
# These steps can work on your files if you replace the filenames and column headers. 

import pandas as pd

df = pd.read_csv("functionalCasg_USETHIS_1182022.csv")

dftest = pd.read_csv("casgFunctionalSample.csv")
  
# Step 1: Fill nan's with empty strings so that len() works properly. 
# Or else len('nan') = 3, which isn't exactly what we want here.
    df.genus = df.genus.fillna("")
    df.species = df.species.fillna("")
    df.taxonRank = df.taxonRank.fillna("")


    # Number of rows with nan taxonRank (should now be 0):
    df.taxonRank.count()

    # Get the unique values that have been entered for the taxonRank field/column (helps to see what we're working with):
    df.taxonRank.unique()


       
          
# Step 2: Define function to fill in taxonRank depending on length of values in genus & species rows.
# Take row as argument, not dataframe as argument, since df.apply() will be used later.
    def label_taxonRank (row): 
        if len(row['genus']) ==0 and len(row['species']) == 0:      # e.g if both genus and species are blank/empty strings
            return row['taxonRank']                                 # Have to return what's there (in the row) already or else you overwrite higher order values like Family, etc
            
        if len(row['genus']) > 0 and len(row['species']) > 0:       # e.g. if genus and species are both filled in, then the taxonRank = species
            return "species"

        if len(row['genus']) > 0 and len(row['species']) == 0:      # e.g. if genus is entered but species isn't, then the taxonRank = Genus
            return "Genus"
            
        
# Step 3: Apply the funcation above to actually fill in values using df.apply().
    df['taxonRank'] = df.apply(label_taxonRank, axis =1)            # axis = 1 applies the function along the column axis, not the index axis (so across the dataframe horizontally instead of up and down the rows)


# Step 4: Define function to fill in scientificName depending on the taxonRank value.    
    def label_scientificName(row):
        if row['taxonRank']== 'Genus':                              # e.g. if taxonRank is Genus then scientificName = whatever was entered in the genus field
            return row['genus']
        if row['taxonRank']=='species':                             # e.g. if taxonRank is species then scientificName = whatever was entered in genus + a blank space + whatever was entered for species
            return row['genus'] + " " + row['species']
        else:
            return row['scientificName']                            # e.g. if there is something other than "Genus" or "species" in taxonRank (like an empty space), return whatever is in scientificName already
                                                                    # This helped not overwrite data when a higher order name was entered for EPICC data (like a Family, etc)
    


dftest['scientificName'] = dftest.apply(label_scientificName, axis =1)  # See how function works on a small set of data rows
    
df['scientificName'] = df.apply(label_scientificName, axis=1)           # Apply to all of data if it seems to be working.

df.to_csv("functionalCASG_editedTaxonRank.csv", index=False)            # Save dataframe with newly populated taxonRanks and scientificNames as csv to be ingested.
   