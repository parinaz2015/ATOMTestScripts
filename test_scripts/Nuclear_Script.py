

from selenium.webdriver.common.by import By
from Reproduce_tables import Reproduce_Column_titles,Reproduce_Data
from fetch_Gnd_Truth_Data.Nuclear_Data import Get_Nuclear_data
import os,ast


#Performs the actual testing. String match for now.
def perform_testing(gnd_truth_table:list, test_table:list, path_to_reports_dir:str):

    Mismatched_Rows = []
    for gnd_truth_row,test_row in zip(gnd_truth_table,test_table):
        diff = set(gnd_truth_row).difference(set(test_row))

        if(len(diff) > 0):
            Mismatched_Rows.append([gnd_truth_row,test_row,diff])

    report_path = os.path.join(path_to_reports_dir, 'Nuclear_report.txt')

    with open(report_path, 'w') as file: 
        if(len(Mismatched_Rows)==0):
            print("No Mismatches between the test and ground truth tables")
        else:
            file.write("Gnd Truth\t\tTest\t\tMismatches(Not displayed as in version 2)")
            for row in Mismatched_Rows:
                file.write("\n"+str(row[0])+"\t"+str(row[1])+"\t"+str(row[2]))

    return


def test_NuclearData(element,driver,gnd_truth_url,path_to_reports_dir):


    #Get the ground truth
    gnd_truth_data_tables = Get_Nuclear_data(element,gnd_truth_url)

    if(gnd_truth_data_tables == []):
        print("Gnd Truth Data not available!Property not tested...")
        return

    # Define the URL (Transition rates url for Li1)
    url = "https://www1.udel.edu/atom/dev/version3/nuclear?element=" + element

    # load the web page
    driver.get(url)

    driver.implicitly_wait(10)

    directory = os.getcwd() + '/Data/Nuclear'

    test_file = element+'test'+'.txt'

    file_path = os.path.join(directory, test_file)
    
    test_data_tables = ''
    test_table_column_titles = ''


    if(os.path.exists(file_path)):
        f = open(file_path)
        test_data_tables = f.read()
        test_data_tables = ast.literal_eval(test_data_tables)
    else:
         #Fetch the tables from the test version: Version 3
        test_table_column_titles = Reproduce_Column_titles(driver)
        test_data_tables = Reproduce_Data(driver)
        if(test_table_column_titles==[] or test_data_tables==[]):
            print("Test Data not available!Property not tested...")
            return

        test_data_tables.insert(0,test_table_column_titles)
        with open(file_path, 'w') as file: 
            file.write(str(test_data_tables))

    perform_testing(gnd_truth_data_tables,test_data_tables,path_to_reports_dir)
    print("Test Complete!Report Generated...")