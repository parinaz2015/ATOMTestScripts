
import os
import csv,glob,re
import requests
import zipfile
import shutil
import re

#Preprocessing data to remove white space
def preprocess(data:list):
    for data_list in data:
        for i in range(0,len(data_list)):
            data_list[i] = data_list[i].replace(" ", "")
    return data


def download_and_unzip(url, destination):
    # Create the directory if it does not exist
    os.makedirs(destination, exist_ok=True)
    
    # Download the zip file
    response = requests.get(url)
    
    # Save the zip file
    zip_file_path = os.path.join(destination, "data.zip")
    
    with open(zip_file_path, "wb") as zip_file:
        zip_file.write(response.content)
    
    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination)
    
    # Remove the _MACOSX folder if it exists
    macosx_folder = os.path.join(destination,"__MACOSX")
    if os.path.exists(macosx_folder):
        shutil.rmtree(macosx_folder)
        # for root, dirs, files in os.walk(macosx_folder):
        #     for file in files:
        #         os.remove(os.path.join(root, file))
        # os.rmdir(macosx_folder)

    # Remove the zip file
    os.remove(zip_file_path)
     # Get the extracted folder path
    # extracted_folder = os.path.join(destination, os.path.splitext(os.path.basename(url))[0])
    
    # # Copy all CSV files from the extracted folder to the destination path
    # csv_files = glob.glob(os.path.join(extracted_folder, '*.csv'))
    # for csv_file in csv_files:
    #     shutil.copy(csv_file, destination)

    #   # Remove the extracted folder and its contents
    # shutil.rmtree(extracted_folder)

def Get_Polarizability_GndTruth_Data(element,path_to_data):

    #Change directory to the where the data is placed.
    download_and_unzip("https://www1.udel.edu/atom/dev/version3/polarizability-files/"+element+"Pol.zip", path_to_data)
    GndTruth_Data_tables = {}
    #List all the extracted CSV files
    csv_files = glob.glob(os.path.join(path_to_data, '*.csv'))

#This block of code is responsible for processing each CSV file found in the specified directory 
    for file_path in csv_files:
        with open(file_path, mode ='r') as file:
            file_content = list(csv.reader(file))
        
        # Remove the first row from the file content
        #file_content = file_content[1:]

        string_with_state = os.path.basename(file_path)#(file_path.split(element+"_"))[1]
        state_string = (string_with_state.split("_Dynamic_"))[0]
        state = state_string.lower() #.replace("_","").replace("-","/")
#2p1.csv 2p3.csv, 2s.csv
        # Keep only the first two columns of file_content
        # Keep only the first two columns of file_content
        #modified_content = [[row[0], row[1]] for row in file_content]
        # Iterate over each header in the first row of file_content
        for i in range(len(file_content[0])):
            # Check if the header contains the string "wavelength"
            if 'wavelength' in file_content[0][i].lower():
                # If found, replace the header with "wavelength"
                file_content[0][i] = "wavelength"
       
        # Define the columns to keep
        columns_to_keep = ["wavelength", "alpha(m=0)", "alpha(m=1)", "alpha(m=2)", "alpha(m=3)"]
        # Compile a regular expression pattern to match any characters before "wavelength"
        # Find the indices of the columns to keep
    # Find the indices of the columns to keep
        indices_to_keep = [file_content[0].index(col) for col in columns_to_keep if col in file_content[0]]

    # Extract the header row with the selected columns
        header_row = [file_content[0][i] for i in indices_to_keep]

    # Extract the data rows with the selected columns
        data_rows = [[row[i] for i in indices_to_keep] for row in file_content[1:]]
        # Find the indices of the columns to keep
#         indices_to_keep = [i for i, col in enumerate(file_content[0]) if pattern.match(col.strip())]

# # Extract the header row with the selected columns
#         header_row = [col.strip() for col in file_content[0] if pattern.match(col.strip())]

# # Extract the data rows with the selected columns
#         data_rows = [[row[i] for i in indices_to_keep] for row in file_content[1:]]
    #     pattern = re.compile('.*wavelength')

    # # Find the indices of the columns to keep
    #     indices_to_keep = [i for i, col in enumerate(file_content[0]) if col.strip() in columns_to_keep]
    
    # # Extract the header row with the selected columns
    #     header_row = [file_content[0][i] for i in indices_to_keep]
    
    # # Extract the data rows with the selected columns
    #     data_rows = [[row[i] for i in indices_to_keep] for row in file_content[1:]]

# Find the indices of the columns to keep
#         indices_to_keep = [file_content[0].index(col) for col in columns_to_keep if col in file_content[0]]

# # Extract the header row with the selected columns
#         header_row = [file_content[0][i] for i in indices_to_keep]

# # Extract the data rows with the selected columns
#         data_rows = [[row[i] for i in indices_to_keep] for row in file_content[1:]]

# Combine the header row and data rows
        modified_content = [header_row] + data_rows

# Print the result
# for row in result:
#     print(row)
        # Store the modified file content in the dictionary with the state as the key
        GndTruth_Data_tables[state] = modified_content
    for state, data_table in GndTruth_Data_tables.items():
    # Print the name of the table (state)
        print("Table Name:", state)
    
    # Print the first row of the table
        if data_table:
            print("First Row:", data_table[0])
        else:
            print("Table is empty")
        # for row in GndTruth_Data_tables[state]:
        # # Print the row
        #     print(row)

#dont delete extra columns        
    return GndTruth_Data_tables