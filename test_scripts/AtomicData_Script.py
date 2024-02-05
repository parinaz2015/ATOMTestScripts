
from selenium.webdriver.common.by import By
from Reproduce_tables import Get_Atomic_Test_Data
from fetch_Gnd_Truth_Data.Atomic_Data import Get_GndTruth_Atomic_data
import numpy as np
import os,itertools

#Splits a list into two lists at a specific element
def split_list(lst, val):
    return [list(group) for k, 
            group in
            itertools.groupby(lst, lambda x: x==val) if not k]


def Remove_Empty_Rows(test_table):

    mismatched_data = []
    empty_rows = 0

    row_indices_to_remove = []
    test_table_without_empty_rows = []
    for i in range(0,len(test_table)):
        test_row = test_table[i]
        if(test_row[0] == '' and all(i == test_row[0] for i in test_row)):
            empty_rows = empty_rows + 1
        else:
            test_table_without_empty_rows.append(test_row)

    return test_table_without_empty_rows


def Check_Missing_Rows_and_Columns(gndTruth_table:list, test_table:list):

    missing_rows = False
    missing_columns = False

    missing_rows = (len(gndTruth_table) != len(test_table))

    ColumnTitles_gndTruth = gndTruth_table[0]
    ColumnTitles_test = test_table[0]

    missing_cols = (len(ColumnTitles_gndTruth) != len(ColumnTitles_test))

    return missing_rows, missing_cols


def Compare_tables(gndTruth_table,test_table,file,table_type):
     #Stores information about the mismatched data
    mismatched_data = []

    #Separate the columns and the actual table data
    gndTruth_table_Column_titles = gndTruth_table[0]
    test_table_Column_titles = test_table[0]

    gndTruth_table_data = gndTruth_table[1]
    test_table_data =test_table[1:]
     
    missing_rows, missing_cols = Check_Missing_Rows_and_Columns(gndTruth_table_data,test_table_data)

    if(missing_rows):
        file.write("\n->Missing rows in test data table: "+ table_type + "\n")
        file.write("->Table not tested")
        file.write("\n--------------------------------------------------------------------------------------------------------------\n")
    
    elif(missing_cols):
        file.write("->Missing columns in test data table: "+ table_type + "\n")
        file.write("->Table not tested")
        file.write("\n--------------------------------------------------------------------------------------------------------------\n")

    else:
        #Testing the Table
        for gndTruth_row, test_row in zip(gndTruth_table_data,test_table_data):
            state = test_row[0]    
            diff = set(gndTruth_row).difference(set(test_row))

            if(len(diff)>0):
                diff_data_to_report = []
                diff = list(diff)
                
                for j in range(0,len(diff)):
                    value_v2 = diff[j]
                    id = gndTruth_row.index(value_v2)
                    Column_title = (gndTruth_table_Column_titles[id]).replace("\n","")
                    value_v3 = test_row[id]
                    diff_data_to_report.append([value_v3,value_v2,Column_title])
                mismatched_data.append([state,diff_data_to_report])

        file.write("\n\nResult for table: "+ table_type+ "\n")
        if(len(mismatched_data)==0):
            file.write("No mismatches between the ground truth and test data")
        else:
            file.write("\nState\t\t\tColumn\t\t\t\t\t\tValue in V3(Test)\t\t\tValue in V2(Ground Truth)")
            file.write("\n--------------------------------------------------------------------------------------------------------------")
            for mismatched_row in mismatched_data:
                state = mismatched_row[0]
                diff_data_to_report = mismatched_row[1]
                
                for row in diff_data_to_report:
                    value_v3 = row[0].replace("\n","")
                    value_v2 = row[1].replace("\n","")
                    Column_title = row[2]
                    file.write("\n"+state+"\t\t"+Column_title+"\t\t\t\t\t\t\t"+value_v3+"\t\t\t\t\t\t\t"+value_v2)

            file.write("\n--------------------------------------------------------------------------------------------------------------")


    return



#Drive the testing of tables
def perform_testing(gnd_truth_table:list, test_table:list, path_to_reports_dir:str):

    report_path = os.path.join(path_to_reports_dir, 'Atomic_report.txt')

    #Get the groud truth tables and the Column titles
    gndTruth_table1 = gnd_truth_table[0]
    gndTruth_table2 = gnd_truth_table[1]

    #Get the test tables and the column titles
    test_table1 = test_table[0]
    test_table2 = test_table[1]

    with open(report_path, 'w') as file:
        Compare_tables(gndTruth_table1,test_table1,file,"Upper")

        if(gndTruth_table2 != [] and test_table2 != []):
            Compare_tables(gndTruth_table2,test_table2,file,"lower")

        file.close()

    return



#Fetching the data tables and performing the testing
def test_AtomicData(element,driver,gnd_truth_url,path_to_reports_dir):

    #Get the ground truth
    gndTruth_Tables = Get_GndTruth_Atomic_data(element,gnd_truth_url)

    if(gndTruth_Tables == []):
        print("Gnd Truth Data not available or does not exist!Property not tested...")
        return

    # # Define the URL (Transition rates url for Li1)
    url = "https://www1.udel.edu/atom/dev/version3/atomic?element=" + element

    # load the web page
    driver.get(url)

    driver.implicitly_wait(10)

    directory = os.getcwd() + '/Data/Atomic'

    test_file = element+'test'+'.txt'

    test_data_tables = ''

    #Fetch the tables from the test version: Version 3
    #The table column titles and the actual data are reproduced separately

    test_data_tables = Get_Atomic_Test_Data(driver)

    if( test_data_tables==[]):
        print("Test Data not available or does not exist!Property not tested...")
        return

    #Perform the testing
    perform_testing(gndTruth_Tables,test_data_tables,path_to_reports_dir)
    print("Test Complete!Report Generated...")
    return