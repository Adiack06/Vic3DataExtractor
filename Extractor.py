import csv
import re
import os
from dotenv import load_dotenv
import glob
import shutil
import threading

load_dotenv()
"""
ISSUES 
whole thing goes boomb if the save is not a binary
it doesnt delete if the save has already been extracted 
implent better comments

"""

def meltsave(save, destination_folder):
    os.system(f"rakaly melt --unknown-key stringify \"{save}\"")
    base_name = os.path.splitext(os.path.basename(save))[0]
    output_file = os.path.join(os.path.dirname(save), f"{base_name}_melted.v3")
    destination = os.path.join(destination_folder, f"{base_name}_melted.v3")
    shutil.move(output_file, destination)
    print(f"{base_name} melted")
    return
def meltsaves(saves, destination_folder):
    threads_limit = 6
    active_threads = []

    for save in saves:
        while len(active_threads) >= threads_limit:
            active_threads = [t for t in active_threads if t.is_alive()]
            threading.Event().wait(0.5)  # Briefly wait for threads to complete

        t = threading.Thread(target=meltsave, args=(save, destination_folder))
        active_threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in active_threads:
        t.join()

    print("All saves melted.")

def extract_eco(save, selected_data_type):
    gdp = False
    with open(f"{save}", "r") as file:
        current_country = None
        values = []
        line_number = 0

        with open(f"{save}output.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for line in file:
                line_number += 1

                if 'definition="' in line:
                    match = re.search(r'definition="(\w+)"', line)
                    if match:
                        current_country = match.group(1)
                        if len(current_country) == 3:
                            gdp = True
                        else:
                            gdp = False

                if selected_data_type in line and gdp:
                    # Skip lines until reaching 'values={'
                    while 'values={' not in line:
                        line = next(file)

                    # Move to the next line where the actual values are located
                    line = next(file)

                    values_str = re.search(r'(\d[\d\s.]+)', line)
                    if values_str:
                        values = [float(val) for val in values_str.group(1).split()]
                        row = [current_country] + values
                        writer.writerow(row)
                        values = []
                        gdp = False

    with open(f"{save}output.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    largest = max(len(row) for row in rows)

    for row in rows:
        num_blank_columns = largest - len(row)
        row[:] = [row[0]] + [''] * num_blank_columns + row[1:]

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
