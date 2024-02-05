# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from test_scripts.MatrixElements_Script import test_MatrixElementData
from test_scripts.TransitionRates_Script import test_TransitionRatesData
from test_scripts.HyperfineData_script import test_HyperfineData
from test_scripts.Nuclear_Script import test_NuclearData
from test_scripts.Energies_Script import test_EnergiesData
from test_scripts.Polarizability_Script import test_PolarizabilityData
from test_scripts.AtomicData_Script import test_AtomicData
from elements import element_data

import os,sys



def test_properties(element,gnd_truth_url,path_to_reports_dir):

    print("========================================================\nTesting Results for",element,":")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print("1. Matrix Elements")
    test_MatrixElementData(element,driver,gnd_truth_url,path_to_reports_dir)

    print("\n2. Transition Rates")
    test_TransitionRatesData(element,driver,gnd_truth_url,path_to_reports_dir)

    print("\n3. Hyperfine Constants")
    test_HyperfineData(element,driver,gnd_truth_url,path_to_reports_dir)

    #print("\n4. Nuclear")
    #test_NuclearData(element,driver,gnd_truth_url,path_to_reports_dir)

    print("\n5. Energies")
    test_EnergiesData(element,driver,gnd_truth_url,path_to_reports_dir)

    print("\n6. Atomic")
    test_AtomicData(element,driver,gnd_truth_url,path_to_reports_dir)

    print("\n6. Polarizability")
    test_PolarizabilityData(element,driver,gnd_truth_url,path_to_reports_dir)

    driver.close()

    return

# Define the ground truth URL for reference
gnd_truth_url = 'https://www1.udel.edu/atom/'

# Get a list of elements from a function called element_data
list_of_elements = element_data("","element list")

# Initialize a list to keep track of elements with completed testing
Elements_with_testing_complete = []

for element in list_of_elements:

    charge_vals = element_data(element,"charge value")

    if(type(charge_vals)==list):
        for val in charge_vals:
            element_with_charge = element + str(val)
            path_to_reports_dir = os.getcwd() + '/reports/' + element_with_charge

            if(os.path.exists(path_to_reports_dir) == False):
                os.mkdir(path_to_reports_dir)
            
            test_properties(element_with_charge,gnd_truth_url,path_to_reports_dir)
            Elements_with_testing_complete.append(element_with_charge)

    else:
        element = element + str(charge_vals)

        path_to_reports_dir = os.getcwd() + '/reports/' + element

        if(os.path.exists(path_to_reports_dir) == False):
            os.mkdir(path_to_reports_dir)

        test_properties(element,gnd_truth_url,path_to_reports_dir)
        Elements_with_testing_complete.append(element)

# Display completion message and the elements with completed testing
print("\n\nTesting complete!! Check the reports directory for generated reports...")
print("Testing completed for following elements:")

for ele in Elements_with_testing_complete:
    print(ele)


# sys.exit()
