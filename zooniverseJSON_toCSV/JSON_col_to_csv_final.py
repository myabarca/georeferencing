'''
Created Jan 12 2021

Modified May 27 2022

This program takes output from our crowd sourced Zooniverse project and turns it into csv format that others can work on and georeference.

The major problem is that locality information is nested in one column of output called annotations where each row in that column is in JSON format.

Things like section/town/range, county, etc are all nested in one cell.

'''

# Use the csv module
import csv

fields = [i for i in range(20)]                        # Define list of fields for the header row/column names. There are 20 columns of relevant info total.
with open("zooniverse_final_testImprovements.csv", "w") as csv_final:            # Open/name a file with write priliveges    
    csvwriter = csv.writer(csv_final)                  # Create instance of csv.writer() class with the csv we'll be writing 
    csvwriter.writerow(fields)                         # Write header row. Will replace numbered headers with more descriptive ones later. 
    with open("from-fossil-fuels-to-fossil-facts-classifications-4.csv", "r") as csv_file:      # Open the Zooniverse data with read privileges
        data = csv.DictReader(csv_file)                                                         # Create instance of csv.DictReader() to read the Zooniverse JSON data in the annotations column.
        for row in data:                        # Each row is a dictionary
            row_list = (row['annotations'])     # We need to parse out what's in the annotations column. The cells contain our data in JSON
            json_list = list(eval(row_list))    # Use eval() to "evaluate" the JSON in that column as a dictionary. Store result in list
            json_value_list = []                # Empty list to append values to
            for item in json_list:              # Each item in the list is now a dictionary
                json_value_list.append(item["value"])   # For each item in the dictionary, append the values only (not the keys). This represents one row of values.
            csvwriter.writerow(json_value_list)         # Write that row of values to the final csv, and then restart loop from beginning to get all rows in data.


