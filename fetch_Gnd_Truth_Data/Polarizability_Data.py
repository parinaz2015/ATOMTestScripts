
import os
import csv,glob,re


#Preprocessing data to remove white space
def preprocess(data:list):
    for data_list in data:
        for i in range(0,len(data_list)):
            data_list[i] = data_list[i].replace(" ", "")
    return data

def Get_Polarizability_GndTruth_Data(element,path_to_data):

    #Change directory to the where the data is placed.

    GndTruth_Data_tables = {}
    #List all the extracted CSV files
    csv_files = glob.glob(path_to_data + '*.csv')

    for file_path in csv_files:
        with open(file_path, mode ='r') as file:
            file_content = list(csv.reader(file))

        string_with_state = (file_path.split(element+"_"))[1]
        state_string = (string_with_state.split("_Dynamic_"))[0]
        state = state_string.replace("_","").replace("-","/")

        GndTruth_Data_tables[state] = file_content

    return GndTruth_Data_tables