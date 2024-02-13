
import os
import csv,glob,re
import requests
import zipfile
import shutil

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
    extracted_folder = os.path.join(destination, os.path.splitext(os.path.basename(url))[0])
    
    # Copy all CSV files from the extracted folder to the destination path
    csv_files = glob.glob(os.path.join(extracted_folder, '*.csv'))
    for csv_file in csv_files:
        shutil.copy(csv_file, destination)

      # Remove the extracted folder and its contents
    shutil.rmtree(extracted_folder)

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
        file_content = file_content[1:]

        string_with_state = (file_path.split(element+"_"))[1]
        state_string = (string_with_state.split("_Dynamic_"))[0]
        state = state_string.replace("_","").replace("-","/")
#2p1.csv 2p3.csv, 2s.csv
        GndTruth_Data_tables[state] = file_content

#dont delete extra columns        
    return GndTruth_Data_tables