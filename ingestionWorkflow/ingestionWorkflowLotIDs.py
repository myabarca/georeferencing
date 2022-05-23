# Created on Thu Dec 9 2021
# Revised Mon May 23 2022




## PART ONE: LOADING THE DATA ##

# Digitized EPICC occurrence records that ended up in our final version for the database came from two main spreadsheets: 
#       1. A sheet that was compiled for all records through 2018, called "epiccThru2018" (downloaded from our department's Google drive)
#       2. A sheet of current specimen data entry, called "epiccSDECurrent" (also downloaded from our department's Google drive)
# These sheets were appended to each other and then called "allEpicc"


import pandas as pd

epiccThru2018 = pd.read_csv('SpecimenDataEntry_through2018 - Specimen Data Entry.csv')

epiccSDECurrent = pd.read_csv('SpecimenDataEntry08062020 - SDE.csv')

allEpicc = epiccThru2018.append(epiccSDECurrent)

# Some minor cleaning steps for allEpicc:

    # The columns for an entered subgenus were denoted two different ways in the two sheets: "subgenus" in SDECurrent and "subGenus" in Thru2018.
    # "subGenus" in Thru2018 was never used (ie always nan), so it was deleted in allEpicc to avoid column redundancy and confusion.
    allEpicc = allEpicc.drop('subGenus', 1)
    #('column_name', 1), axis = 1 is columns. 

    # There were also some holdover columns added to the source Google sheets that came from the historical Filemaker database.
    # These were removed to avoid redundancy later on.
    allEpicc = allEpicc.drop(['description', 'dimensions cm', 'marking field','page #s', 'KINGDOM', 'PHYLUM', 'REFERENCE NOTES', 'TAXA'], 1)

## New epicc sheet to edit from now on: 
allEpicc.to_csv('allEpicc.csv', index=False)


# Show summary of the data
allEpicc.info()



# For historical records, all the records in the Filemaker database were exported to a csv. 
# Header columns were added to the csv since the Filemaker doesn't include headers in exports.
# Date formats were changed to YYYY-MM-DD using Open Refine
# Some records had empty accession number fields in Filemaker. Those were reviewed and removed from the final csv. 

FM = pd.read_csv('FM-lotdump11082021-edited-with-headers-editedDatesAndNoBlankAccnIDs-openRefine.csv')

# Show summary of the data
FM.info()


## PART TWO: CHECKING FOR PROBLEMATIC LOTS BASED ON DUPLICATE NUMBERS ##

# Because several workers were digitizing records for EPICC at the same time in separate Google sheets, and because lots are often split in different parts of the physical collection space, 
# some lots with the same unique identifier (lotID in this case), were entered more than once without people knowing. 
# These instances need to be reviewed and corrected before ingestion. 

# Coming up with checklist of duplicate lotIDs in allEpicc with some feature engineering: 

    # Add a column that is True when a lotID is duplicated, and False when it's unique
    allEpicc['dupLotID']=allEpicc.duplicated(subset=['lotID'], keep=False)  # keep=False marks all duplicates, instead of just excluding the first or last occurrence
    
    # Filter the data where duplicate = True and store in a new dataframe
    df_dupLotIDsallEpicc = allEpicc[allEpicc['dupLotID']==True]

    # Save that new dataframe as a csv to review duplications
    df_dupLotIDsallEpicc.to_csv('allEpiccDuplicateLots.csv', index=False)

    # After review, a lot of records were duplicated because they appeared in both of the source sheets mentioned above in Part One. 
    # So, we will go through and keep only one of the identical records later.  
    # Other lotIDs were duplicated because of inconsistent use of a field we called "specimenID"
    # Others because at some point a lot was split into different physical locations in the collection, and then different workers digitized each part of the lot independently. 
    # These will all need review later, but for now we will remove them from the final data.
    

# Coming up with checklist of lotIDs that are used in both the new allEpicc and historic Filemaker export

# Because the Epicc work was done in Google sheets that were not connected to the Filemaker database, 
# and because some lots in Filemaker were already cataloged and within Epicc's scope, 
# some lotID's were duplicated between the two sources. 
# These records need to be isolated and reviewed as well. 

    # Creating a set of each column's values gives you a unique list of values for comparison
    fmLots = set(FM['lotID'])   # for Filemaker

    epiccLots = set(allEpicc['lotID'])  # for Epicc

    # Where these sets overlap is where we'll have data integrity issues later.
    # We get the overlap by applying intersection (&)
    set_overlapLots = fmLots.intersection(epiccLots)    # You could also use overlapLots = fmLots & epiccLots

    # We'll also need to isolate the duplicates within just the Epicc data
    set_dupLotsAllEpicc = set(df_dupLotIDsallEpicc['lotID']) 

    # All of our "problem" lotIDs then are represented by combining the overlap between Filemaker and Epicc with the duplicates in the Epicc data
    set_problemLots = set_overlapLots | set_dupLotsAllEpicc     # | represents the "logical OR"


## PART THREE: ISOLATING AND REMOVING PROBLEMATIC LOTS BASED ON DUPLICATE NUMBERS ##

# These issues with duplicated lotIDs will require manual review by collections staff. 
# Reviewing and correcting the ~700 records will take time, so for now we are isolating and removing these "problematic lots" and will add them back into the final database as they're corrected. 

    # Filter the allEpicc data by lotIDs that are in our "problems" overlap set 
    df_problemLots = allEpicc[allEpicc['lotID'].isin(set_overlapLots)]

    # Save records as csv to review later.
    df_problemLots.to_csv('inFMandEPICC.csv', index=False)

    # Filter out "problem" lotIDs from epicc data 
    functionalEpicc = allEpicc[~allEpicc['lotID'].isin(set_problemLots)]

    # Can also drop dupLotID column now
    functionalEpicc = functionalEpicc.drop('dupLotID', 1)

    # Filter out "problem" lotIDs from Filemaker data
    functionalFM = FM[~FM['lotID'].isin(set_problemLots)]


## PART FOUR: ASSEMBLING "FUNCTIONAL" RECORDS INTO ONE DATASET FOR INGESTION##

# Before appending the "functionalEpicc" and "funcationalFM" dataframes together, the headers for columns that hold congruent data need to match in order to maintain integrity. Not all columns need to be shared, 
# but those columns that contain the same data between the sources need to have matching headers. 
# For example, the "collector" header in Filemaker was changed to "recordedBy" to match the Epicc header for this field.
# These new version were then loaded in and used going forward (old versions with old headers were archived)

functionalEpicc_edited = pd.read_csv('functionalEpicc_v3_headersEdited.csv')
functionalFM_edited = pd.read_csv('functionalFM_v3_headersEdited.csv')

# Additionally, the Filemaker data was missing columns for institutionCode, collectionCode, basisOfRecord, and occurrenceID (all present in Epicc data); so those were added: 
functionalFM_edited['institutionCode']= 'CASG'
functionalFM_edited['collectionCode']= 'FOSSIL'
functionalFM_edited['basisOfRecord']= 'FossilSpecimen'
functionalFM_edited['occurrenceID']= 'urn:' + 'catalog:' + 'CASG:' + 'FOSSIL:' + functionalFM_edited['lotID'].astype(str)

# Now that the headers were sorted, the dataframes were appended:
combine = functionalEpicc_edited.append(functionalFM_edited)    # concat also works: combine_concat = pd.concat([functionalEpicc_edited,functionalFM_edited])

# Save result to csv and use this final version to ingest into database.
combine.to_csv('functionalEpiccAndFMCombined.csv', index=False)





    