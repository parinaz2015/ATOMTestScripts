
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
        #iterates through each state in the "GndTruth_data" dictionary. It checks if the state exists in both "GndTruth_data" and "Test_data". 
        #If not, it logs a message indicating that testing was not performed for that state.
        for state in States_GndTruth:
            GndTruth_Table = GndTruth_data[state]
            # print("\nGndTruth_Table =", GndTruth_Table)
            Header_GndTruth = GndTruth_Table[0]

            if state not in Test_data:
                file.write("State " + state + " not found in Test data.\n")
                file.write("No Testing performed for this state.\n")
                file.write("----------------------------------------------------------------------------\n")
                continue  # Skip to the next state if test data for this state is missing


            Test_Table = Test_data[state]
            # print("\n\nTest_Table =", Test_Table)
            Header_Test = Test_Table[0]

            if(Header_GndTruth != Header_Test):
                Missing_Column_titles = []
                #If the header lengths do not match, it identifies and logs any missing column titles in the "Test_data" table for that state.
                for title in Header_GndTruth:
                    if(title not in Header_Test):
                        Missing_Column_titles.append(title)
                Header_GndTruth = GndTruth_Table[0]
                Header_Test = Test_Table[0]
                file.write("\n\nMissing Columns in Test Data for state: "+ state+ " , No Testing performed!\n")
                #file.write("Missing Columns: " + ', '.join(Missing_Column_titles) + "\n")
                # file.write("\nHeader_GndTruth =", Header_GndTruth)
                # file.write("Header_Test =\n", Header_Test)
                file.write("Header_GndTruth = " + str(Header_GndTruth)+"\t" )
                file.write("Header_Test = " + str(Header_Test) + "\n")
                file.write("----------------------------------------------------------------------------\n")
                mismatch_found = True
            else:
                # Compare data content
                # file.write(f"State: {state}\n")
                # file.write(f"      [row_index]  [     GndTruth Data     ]   [     Test Data     ]\n")
                # file.write(f" ===========================================")
                # max_rows = min(len(GndTruth_Table), len(Test_Table))
                # for row_idx in range(1, max_rows):
                #     if GndTruth_Table[row_idx] != Test_Table[row_idx]:
                #         file.write(f"\nMismatch {row_idx}.")
                #         file.write(f"{GndTruth_Table[row_idx]}")
                #         file.write(f"{Test_Table[row_idx]}")
                #         mismatch_found = True
                #         #break
                #mismatches_found = False
                wavelength_idx = Header_GndTruth.index('wavelength')  # Assuming 'wavelength' is the column name
                wavelengths_GndTruth = {row[wavelength_idx]: row for row in GndTruth_Table[1:]}
                wavelengths_Test = {row[wavelength_idx]: row for row in Test_Table[1:]}

                common_wavelengths = sorted(set(wavelengths_GndTruth.keys()) & set(wavelengths_Test.keys()), key=lambda x: float(x))
                file.write(f"\n\nState: {state}\n")
                file.write(f"Mismatch  [     GndTruth Data     ]   [     Test Data     ]\n")
                file.write(f" ===========================================\n")
                for wavelength in common_wavelengths:
                    if wavelengths_GndTruth[wavelength] != wavelengths_Test[wavelength]:
                        mismatch_found = True
                        #file.write(f"Mismatch  wavelength {wavelength}.\n")
                        file.write(f"{wavelengths_GndTruth[wavelength]}")
                        file.write(f"{wavelengths_Test[wavelength]}\n")

                missing_wavelengths = set(wavelengths_GndTruth.keys()) ^ set(wavelengths_Test.keys())
                if missing_wavelengths:
                    file.write("\n\nMissing wavelengths  [     GndTruth Data     ]   [     Test Data     ]\n")
                    for missing_wavelength in sorted(missing_wavelengths, key=lambda x: float(x)):
                        gndtruth_row = wavelengths_GndTruth.get(missing_wavelength, "Not Found")
                        test_row = wavelengths_Test.get(missing_wavelength, "Not Found")
                        # Check if other columns have values more than 5000 or less than -5000
                        if gndtruth_row != "Not Found":
                            other_columns_values = [float(val) for val in gndtruth_row if val != missing_wavelength]
                            if any(abs(val) > 5000 for val in other_columns_values):
                                continue
                        file.write(f"Missing {missing_wavelength}: [{gndtruth_row}] [{test_row}]\n")

                # file.write(f"\n\nMissing wavelengths  [     GndTruth Data     ]   [     Test Data     ]\n")
                # for missing_wavelength in missing_wavelengths:
                #     file.write(f"wavelength {missing_wavelength}.\n")

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