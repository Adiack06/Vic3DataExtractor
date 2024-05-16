import csv
import re
import os
import zipfile



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

def count_columns(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        first_row = next(reader, None)  # Get the first row, or None if empty
        if first_row:
            return len(first_row)
        else:
            return 0  # Return 0 if the file is empty
def mergecsv():
    Columns_done = 0
    # Check if merged_data.csv exists, if not, create it with a header row
    if not os.path.exists("merged_data.csv"):
        with open("merged_data.csv", 'w', newline='') as merged_file:
            writer = csv.writer(merged_file)
            # Write header row
            writer.writerow(["Country ID", "Column1", "Column2", ...])  # Add column names as needed

    # Get a list of all CSV files in the Extracted_saves directory
    csv_files = sorted([f for f in os.listdir("Extracted_saves") if f.endswith('.csv')])


    # Iterate through each CSV file
    for csv_file in csv_files:
        with open(os.path.join("Extracted_saves", csv_file), 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                country_id = row[0]  # Assuming the first column contains the country ID

                # Check if the country ID exists in merged_data.csv
                with open("merged_data.csv", 'r') as merged_file:
                    merged_reader = csv.reader(merged_file)
                    id_exists = any(country_id in merged_row for merged_row in merged_reader)

                # Append the row to merged_data.csv if the country ID doesn't exist
                if not id_exists:
                    with open("merged_data.csv", 'a', newline='') as merged_file:
                        writer = csv.writer(merged_file)
                        writer.writerow(row)
                else:
                    # If the ID exists, find the matching row in merged_data.csv
                    with open("merged_data.csv", 'r') as merged_file:
                        merged_reader = csv.reader(merged_file)
                        merged_rows = list(merged_reader)  # Read all rows into memory
                        for merged_row in merged_rows:
                            if country_id in merged_row:
                                # Find the index where the ID is located
                                index = merged_row.index(country_id)
                                # Append the values from the current row to the existing row in merged_data.csv
                                merged_row.extend(row[Columns_done+1:])  # Append data after the last column of existing row
                                break
                    # Rewrite merged_data.csv with updated rows
                    with open("merged_data.csv", 'w', newline='') as merged_file:
                        writer = csv.writer(merged_file)
                        writer.writerows(merged_rows)
            Columns_done = count_columns(os.path.join("Extracted_saves", csv_file))
            print(f"Save Added, {Columns_done} Columns Completed")

files = os.listdir(os.path.dirname(os.path.abspath(__file__)))
print(files)

for i in files:
    if ".v3" in i:
        unzip(i)

files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Extracted_saves"))

for i in files:
    extract_eco(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Extracted_saves",i))

mergecsv()