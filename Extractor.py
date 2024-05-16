import csv
import re
import os
import zipfile
import pandas as pd



def unzip(zip_file):
   # Get the absolute path of the directory containing the Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Extract the file name and extension from the zip file path
    file_name, _ = os.path.splitext(zip_file)
    
    # Create the directory for extraction (same name as the zip file)
    extract_to = os.path.join(script_dir,"Extracted_saves", file_name)
    os.makedirs(extract_to, exist_ok=True)
    
    # Extract the contents of the zip file to the created directory
    files = script_dir
    if not file_name in files:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

def extract_eco(save):
    gdp = False
    with open(f"{save}/gamestate", "r") as file:
        # Initialize variables to store country and values
        current_country = None
        values = []

        # Open CSV file for writing
        with open(f"{save}output.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Iterate over each line in the file
            for line in file:
                # Check if the line contains the specified definition
                if 'definition="' in line:
                    # Extract the country name
                    match = re.search(r'definition="(\w+)"', line)
                    if match:
                        current_country = match.group(1)
                        # Check if the country name is three letters long
                        if len(current_country) == 3:
                            gdp = True
                        else:
                            gdp = False

                # Check if the line contains the values
                if 'values={' in line and gdp:
                    # Extract the values
                    values_str = re.search(r'values={(.+?)}', line)
                    if values_str:
                        values = [float(val) for val in values_str.group(1).split()]
                        # Write to CSV
                        row = [current_country] + values
                        writer.writerow(row)
                        # Reset values for next country
                        values = []
                        gdp = False

    # Reopen the output.csv file to modify
    with open(f"{save}output.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    # Determine the largest number of columns
    largest = max(len(row) for row in rows)

    # Add blank columns after the first column if needed
    for row in rows:
        num_blank_columns = largest - len(row)
        row[:] = [row[0]] + [''] * num_blank_columns + row[1:]

    # Write back to the output.csv file
    with open(f"{save}output.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

def mergecsv():
    csv_files = [file for file in os.listdir("Extracted_saves") if file.endswith(".csv")]
    # Initialize an empty DataFrame to store the merged data
    merged_df = pd.DataFrame()

    # Loop through each CSV file
    for file in csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(os.path.join("Extracted_saves", file), index_col=0)

        # Merge the DataFrame with the existing merged DataFrame using the common key column
        merged_df = merged_df.combine_first(df)

    # Replace null values with non-null values
    merged_df.ffill(inplace=True)
    merged_df.to_csv("merged_data.csv")

    # Step 1: Optimize data types if necessary
    # Ensure that 'key' columns are of the same data type
    df1['key'] = df1['key'].astype(int)
    df2['key'] = df2['key'].astype(int)

    # Step 2: Set index for faster merging
    df1.set_index('key', inplace=True)
    df2.set_index('key', inplace=True)

    # Step 3: Merge the DataFrames using appropriate merge method
    merged_df = df1.merge(df2, how='inner', left_index=True, right_index=True)

    # Step 4: Reset index if needed
    merged_df.reset_index(inplace=True)


files = os.listdir(os.path.dirname(os.path.abspath(__file__)))

print(files)

for i in files:
    if ".v3" in i:
        unzip(i)

files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Extracted_saves"))

for i in files:
    extract_eco(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Extracted_saves",i))

# Call the mergecsv function to merge the CSV files
mergecsv()