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


def mergecsv():
    # Directory where the extracted save files are located
    extract_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Extracted_saves")

    # Collect all CSV file paths
    csv_files = []
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    # Dictionary to hold merged data
    merged_data = {}
    time_points = set()

    # Read each CSV file and gather all time points
    for file in csv_files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                country_code = row[0]
                values = row[1:]
                if country_code not in merged_data:
                    merged_data[country_code] = []
                time_points.update(range(1, len(values) + 1))

    # Convert the time points set to a sorted list
    time_points = sorted(time_points)

    # Initialize the data structure with empty lists for each time point
    for country_code in merged_data.keys():
        merged_data[country_code] = [''] * len(time_points)

    # Read each CSV file again and place values in the correct positions
    for file in csv_files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                country_code = row[0]
                values = row[1:]
                for i, value in enumerate(values):
                    if value:
                        merged_data[country_code][i] = value

    # Write the merged data to a new CSV file
    with open('merged_output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Country'] + [f'Time {tp}' for tp in time_points]
        writer.writerow(header)
        for country_code, values in merged_data.items():
            row = [country_code] + values
            writer.writerow(row)
files = os.listdir(os.path.dirname(os.path.abspath(__file__)))

print(files)

for i in files:
    if ".v3" in i:
        unzip(i)

files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Extracted_saves"))

for i in files:
    extract_eco(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Extracted_saves",i))
mergecsv()