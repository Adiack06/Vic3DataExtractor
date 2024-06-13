import csv
import re
import os
from dotenv import load_dotenv
import glob
import shutil

load_dotenv()
"""
ISSUES 
whole thing goes boomb if the save is not a binary

"""

def meltsave(save, destination_folder):
    os.system(f"rakaly melt --unknown-key stringify \"{save}\"")
    base_name = os.path.splitext(os.path.basename(save))[0]
    output_file = os.path.join(os.path.dirname(save), f"{base_name}_melted.v3")
    destination = os.path.join(destination_folder, f"{base_name}_melted.v3")
    shutil.move(output_file, destination)
    return destination
def meltsaves(save_folder, destination_folder):
    saves = glob.glob(os.path.join(save_folder, "*.v3"))
    for save in saves:
        os.system(f"rakaly json --unknown-key stringify \"{save}\"")

        base_name = os.path.splitext(os.path.basename(save))[0]
        output_file = os.path.join(save_folder, f"{base_name}_melted.v3")
        destination = os.path.join(destination_folder, f"{base_name}_melted.v3")
        shutil.copy(output_file, destination)
        print(f"Processed {len(saves)} save files.")

def extract_eco(save ,selected_data_type):
    gdp = False
    with open(f"{save}", "r") as file:
        # Initialize variables to store country and values
        current_country = None
        values = []
        line_number = 0  # Track the line number

        # Open CSV file for writing
        with open(f"{save}output.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Iterate over each line in the file
            for line in file:
                line_number += 1  # Increment line number
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
                if selected_data_type in line and gdp:
                    # Move to the line 7 lines below
                    for _ in range(7):
                        line = next(file)
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





def mergecsv(extract_dir):
    csv_files = []
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    merged_data = {}
    time_points = set()

    for file in csv_files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data_type = row[0]
                country_code = row[1]
                values = row[2:]
                key = (data_type, country_code)
                if key not in merged_data:
                    merged_data[key] = []
                time_points.update(range(1, len(values) + 1))

    time_points = sorted(time_points)

    for key in merged_data.keys():
        merged_data[key] = [''] * len(time_points)

    for file in csv_files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data_type = row[0]
                country_code = row[1]
                values = row[2:]
                key = (data_type, country_code)
                for i, value in enumerate(values):
                    if value:
                        merged_data[key][i] = value

    with open('merged_output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Data Type', 'Country'] + [f'Time {tp}' for tp in time_points]
        writer.writerow(header)
        for key, values in merged_data.items():
            row = list(key) + values
            writer.writerow(row)

    return 'merged_output.csv'
