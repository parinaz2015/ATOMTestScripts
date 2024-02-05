
from selenium.webdriver.common.by import By
from Reproduce_tables import Reproduce_Column_titles,Reproduce_Data
from fetch_Gnd_Truth_Data.TransitionRates_Data import Get_TransitionRates_GndTruth_Data
import os , ast

#Performs the actual testing
def Perform_Testing(gnd_truth_data:dict,gnd_truth_exp_data:bool,test_data:dict,path_to_reports_dir:str):

    report_path = os.path.join(path_to_reports_dir, 'TransitionRates_report.txt')
    if(len(gnd_truth_data.keys()) == len(test_data.keys())):
 
        states_list = list(gnd_truth_data.keys())

        mismatched_radiativeLifetimes_data = []
        mismatched_exp_data = []
        mismatched_transitionRates_data = []

        States_With_Missing_RadiativeLiftimes_data = []
        States_With_Missing_Exp_data = []
        States_With_Missing_TransitionRates_data = []

        for state in states_list:

            #Retrieving the test data for the state
            gnd_truth_data_tables = gnd_truth_data[state]

            test_data_tables = test_data[state]

            Column_titles = test_data_tables[0]

            #Separate out the radiative lifetimes and transition rates data
            #1. Separation For Ground truth
            gndTruth_radiativeLifetimes_data = gnd_truth_data_tables[0]

            gnd_truth_exp_data = []
            if(gnd_truth_exp_data):
                gnd_truth_exp_data = gnd_truth_data_tables[1]
                gndTruth_transitionRates_data = gnd_truth_data_tables[2:]
                test_radiativeLiftimes_data = test_data_tables[1][0]
                test_exp_data = test_data_tables[1][1]
                test_transitionRates_data = test_data_tables[1][1:]
            else:
                gndTruth_transitionRates_data = gnd_truth_data_tables[1:]
                test_radiativeLiftimes_data = test_data_tables[1][0]
                test_transitionRates_data = test_data_tables[1][1:]


            #Test the radiative lifetimes data. Also checks if theres missing data
            if(len(gndTruth_radiativeLifetimes_data) == len(test_radiativeLiftimes_data)):   

                diff = set(gndTruth_radiativeLifetimes_data).difference(set(test_radiativeLiftimes_data))
                if(len(diff) > 0):
                    value_v3 = test_radiativeLiftimes_data[1]
                    value_v2 = gndTruth_radiativeLifetimes_data[1]
                    mismatched_radiativeLifetimes_data.append([state,[value_v3,value_v2]])

            else:
                States_With_Missing_RadiativeLiftimes_data.append(state)

               #Test the radiative lifetimes data. Also checks if theres missing data
            if(gnd_truth_exp_data):
                if(len(gnd_truth_exp_data) == len(test_exp_data)):   

                    diff = set(gnd_truth_exp_data).difference(set(test_exp_data))
                    if(len(diff) > 0):
                        mismatched_exp_data.append([state,To_state,diff])

                else:
                    States_With_Missing_Exp_data.append(state)


            #Test the transition rates data
            if(len(gndTruth_transitionRates_data) == len(test_transitionRates_data)):

                for test_row in test_transitionRates_data:
                    To_state = test_row[1]
                    for gndTruth_row in gndTruth_transitionRates_data:
                        if(To_state == gndTruth_row[1]):
                            diff = set(gndTruth_row).difference(set(test_row))
                            if(len(diff) > 0):
                                diff = list(diff)
                                diff_data_to_report = []
                                for j in range(0, len(diff)):
                                    value_v2 = diff[j]
                                    id = gndTruth_row.index(value_v2)
                                    Column_title = (Column_titles[id]).replace("\n","")
                                    Column_title = Column_title.replace("info","")
                                    value_v3 = test_row[id]
                                    diff_data_to_report.append([value_v3,value_v2,Column_title])

                                mismatched_transitionRates_data.append([state,To_state,diff_data_to_report])

            else:
                States_With_Missing_TransitionRates_data.append(state)


        with open(report_path, 'w') as file: 
            file.write("Mismatched Radiative Lifetimes data:")
            file.write("\nState\t\tValue in V3(Test)\t\t\tValue in V2(Ground Truth)")
            for mismatched_row in mismatched_radiativeLifetimes_data:
                state = mismatched_row[0]
                value_v3 = (mismatched_row[1][0]).replace("\n","")
                value_v2 = (mismatched_row[1][1]).replace("\n","")
                if("Ref" in value_v3):
                    file.write("\n"+state+"\t\t"+value_v3+"  \t\t\t"+value_v2)
                else:
                    file.write("\n"+state+"\t\t"+value_v3+"       \t\t\t"+value_v2)

            file.write("\n==================================================================================\n")

            if(gnd_truth_exp_data):
                file.write("Mismatched Experimental data:")
                file.write("\nFrom\tTo\t\tMismatched strings (Not displayed as in version 2)")
                for mismatched_row in mismatched_exp_data:
                    state_from = mismatched_row[0]
                    state_to = mismatched_row[1]
                    file.write("\n"+state_from+"\t"+state_to+"\t\t"+str(mismatched_row[2]))

                file.write("\n==================================================================================\n")
                        
            file.write("\nMismatched Transition Rates data:")
            file.write("\nFrom\tTo\t\t\tColumn\t\t\t\t\t\tValue in V3(Test)\t\t\tValue in V2(Ground Truth)")
            for mismatched_row in mismatched_transitionRates_data:
                state_from = mismatched_row[0]
                state_to = mismatched_row[1]
                diff_data_to_report = mismatched_row[2]

                for row in diff_data_to_report:
                    value_v3 = row[0].replace("\n","")
                    value_v2 = row[1].replace("\n","")
                    Column_title = row[2]
                    file.write("\n"+state_from+"\t"+state_to+"\t\t"+Column_title+"  \t\t\t    "+value_v3+"\t\t\t\t    "+value_v2)

                file.write("\n--------------------------------------------------------------------------------------------------------------")


            
    else:
        with open(report_path, 'w') as file: 
            file.write("No. of states in the ground truth and test table are equal")
            file.write("Testing cannot be performed until data for missing states is added")

    return
        
        
        

def fetch_test_data_tables(driver,test_url,file_path):
     # load the web page
    driver.get(test_url)

    driver.implicitly_wait(10)

    num_clicks_on_More_states = 2

    TransitionRates_data_tables = {}

    # click on the "More stated" button to reveal more states
    while(num_clicks_on_More_states>0):

        btn_state_text = "//button[text()='More states']"
        
        try:
            More_states_btn = driver.find_element(By.XPATH, btn_state_text)
        except:
            return TransitionRates_data_tables


        More_states_btn.click()
        num_clicks_on_More_states = num_clicks_on_More_states - 1


    #Get all the buttons
    try:
        btns_grid_list = driver.find_elements(By.XPATH,"//div[contains(@class, 'flex ml-4')]")
    except:
        return TransitionRates_data_tables
        
    if (btns_grid_list[0].text==''):
        return TransitionRates_data_tables

    btns_grid_text = btns_grid_list[0].text

    displayed_btns_lst = list(btns_grid_text.split("\n"))
    analyzed_btns_states = []

    #Start clicking the buttons and reproducing the tables
    for btn in displayed_btns_lst:
        btn_chars = list((btn.split("/"))[0])
        btn_chars.pop()
        btn_state = ''
        for charac in btn_chars:
           btn_state = btn_state + charac
      
        if(btn_state not in analyzed_btns_states):
            btn_state_text = "//button[text()='" + btn_state + "']"
            buttons_list = driver.find_elements(By.XPATH, btn_state_text)
            for btn in buttons_list:
                btn.click()

                #Reproduce the column titles first
                reproduced_titles = Reproduce_Column_titles(driver)
                #Reproduces the data in columns
                reproduced_data = Reproduce_Data(driver)

                TransitionRates_data_tables[btn.text] = [reproduced_titles,reproduced_data]
            
            analyzed_btns_states.append(btn_state)

    #Write the test tables to the file
    with open(file_path, 'w') as file: # saves modified html doc
        file.write(str(TransitionRates_data_tables))      

    return TransitionRates_data_tables  





def test_TransitionRatesData(element,driver,gnd_truth_url,path_to_reports_dir):
    # Define the URL (Transition rates url for Li1)

    test_url = "https://www1.udel.edu/atom/dev/version3/transition?element="+element

    # Get the Ground truth data
    GndTruth_TR_data_tables,GndTruth_Exp_Data_Exists = Get_TransitionRates_GndTruth_Data(element,gnd_truth_url)
    if(GndTruth_TR_data_tables == []):
        print("Ground Truth Data not available!Property not tested...")
        return

    #Set the path for the test file to be written to
    directory = os.getcwd() + '/Data/TransitionRates'

    test_file = element+'test'+'.txt'

    file_path = os.path.join(directory, test_file)

    test_data_tables = ''
    #Fetch the test data tables
    if(os.path.exists(file_path)):                      #Temporary for testing!! Needs to be removed
        f = open(file_path)
        test_data_tables = f.read()
        test_data_tables = ast.literal_eval(test_data_tables)
    else:
        test_data_tables = fetch_test_data_tables(driver,test_url,file_path)
        if(test_data_tables == {}):
            print("Test Data not available!Property not tested...")
            return
    
    #Perform the actual testing
   
    Perform_Testing(GndTruth_TR_data_tables,GndTruth_Exp_Data_Exists, test_data_tables,path_to_reports_dir)
    print("Test Complete!!Report Generated...")