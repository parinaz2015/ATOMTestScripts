
import requests
import json

import os,sys
from fetch_Gnd_Truth_Data.Polarizability_Data import Get_Polarizability_GndTruth_Data
from Reproduce_tables import Get_Polarizability_Test_Data


# query = """
# query GetElementQuery($title: String) {
#   element(title: $title) {
#     id
#     title
#     titleDisplay
#     NISTASDTitle
#     isMatrixElements
#     isTransitionRates
#     isEnergies
#     isNuclears
#     isHyperfineConstants
#     isPolarizabilities
#     isStaticPolarizabilities
#     isHCIEnergies
#     isHCITransitions
#     dynamicPolarizabilities {
#       state
#       wavelength
#       alpha
#       __typename
#     }
#     matrixElements {
#       stateOne
#       initialEnergy
#       __typename
#     }
#     __typename
#   }
# }
# """

# def fetch_test_data_from_database()->dict:
# # we have imported the requests modul


#     # defined a URL variable that we will be
#     # using to send GET or POST requests to the API
#     url = "https://atom.ece.udel.edu/graphql"
    

#     response = requests.post(url=url, json={"query": query})

#     if response.status_code != 200:
#         print("No response!Check query\nStatus code: ", response.status_code)
#         sys.exit()


#     response_String =  response.content.decode('utf-8')
#     json_obj = json.loads(response_String)
#     data_json = list(json_obj.values())
#     data = data_json.pop()
#     response_data = (dict(data['element']))
#     polData_list = list(response_data['dynamicPolarizabilities'])

#     test_data = {}
#     states_list = []
#     for dict_entry in polData_list:
#         state = dict_entry['state']
#         if(state not in states_list):
#             test_data[state] = []
    
#     for dict_entry in polData_list:
#         state = dict_entry['state']
#         wavelength = dict_entry['wavelength']
#         alpha = dict_entry['alpha']
#         list_wavelength = test_data[state]
#         list_wavelength.append((wavelength,alpha))

#     return test_data
    
#Creates a directory if it doesn't exist
def create_directory(path):

    if(os.path.exists(path) == False):
        os.mkdir(path)

    return


#Perform the actual testing
def perform_testing(GndTruth_data:dict,Test_data:dict,path_to_reports_dir:str):

    States_GndTruth = list(GndTruth_data.keys())

    report_path = os.path.join(path_to_reports_dir, 'Polarizability_report.txt')

    with open(report_path, 'w') as file:
        #First check if the ground truth and test tables have equal number of columns
        #If yes proceed, if no stop.
        mismatch_found = False  # Flag to track if any mismatches were found
        for state in States_GndTruth:
            GndTruth_Table = GndTruth_data[state]
            Header_GndTruth = GndTruth_Table[0]

            if state not in Test_data:
                file.write("State " + state + " not found in Test data.\n")
                file.write("No Testing performed for this state.\n")
                file.write("----------------------------------------------------------------------------\n")
                continue  # Skip to the next state if test data for this state is missing


            Test_Table = Test_data[state]
            Header_Test = Test_Table[0]

            if(len(Header_GndTruth) != len(Header_Test)):
                Missing_Column_titles = []
                for title in Header_GndTruth:
                    if(title not in Header_Test):
                        Missing_Column_titles.append(title)

                file.write("Missing Columns in Test Data for state: "+ state+ " , No Testing performed!\n")
                file.write("Missing Columns: " + ', '.join(Missing_Column_titles) + "\n")
                file.write("----------------------------------------------------------------------------\n")
                mismatch_found = True

            if not mismatch_found:
                file.write("No mismatches found for state: "+ state+ ", Test completed successfully.\n")
                file.write("----------------------------------------------------------------------------\n")
    return


def test_PolarizabilityData(element,driver,gnd_truth_url,path_to_reports_dir):

     # # Define the URL to download test data
    test_url = "https://www1.udel.edu/atom/dev/version3/polarizability?element=" + element

    current_directory = os.getcwd()
    #Path to the data directory
    data_directory = current_directory + '/Data/Polarizability/' + element

    GndTruth_data_directory = data_directory + '/GndTruth/'

    Test_data_directory = data_directory + '/Test/'

    for directory in [data_directory,GndTruth_data_directory,Test_data_directory]:
        create_directory(directory)
   
    #Get the ground truth data (Data from the physicists)
    # Automate download of the ground truth csv files
    GndTRuth_data_tables = Get_Polarizability_GndTruth_Data(element,GndTruth_data_directory)
    if(GndTRuth_data_tables == {}):
        print("Ground Truth Data not available or does not exist!Property not tested...")
        return

    #Download the test data: Version 3 data
    #Note: The test data is the downloaded data and is in the form of a dictionary with 
    #      a state as the key and the corresponding data as the value.

    test_data_tables = Get_Polarizability_Test_Data(driver,test_url,Test_data_directory,element)

    if(test_data_tables == {}):
        print("Test Data not available or does not exist!Property not tested...")
        return
    
    perform_testing(GndTRuth_data_tables,test_data_tables,path_to_reports_dir)

    return