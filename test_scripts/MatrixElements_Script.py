
from selenium.webdriver.common.by import By
from Reproduce_tables import Reproduce_Column_titles,Reproduce_Data
from fetch_Gnd_Truth_Data.Matrix_Elements_Data import Get_MatrixElements_data
import os,ast,sys


#Performs the actual testing
def Perform_Testing(gnd_truth_data:dict,test_data:dict,path_to_reports_dir:str):
    gnd_truth_states_list = list(gnd_truth_data.keys())
    test_data_states_list = list(test_data.keys())

    # Check for missing states
    missing_states = []
    for state in test_data_states_list:
        if((state in gnd_truth_states_list) == False):
            missing_states.append(state)

    mismatched_data = []
    if(len(missing_states)>0):
        print("Number of missing states = ", len(missing_states))
        print("Further Consistency Check aborted!")
    else:
        # Fetch the appropriate data rows from the ground truth and test tables corresponding
        # to a state and compare.
        for state in gnd_truth_states_list:
            gnd_truth_frame = gnd_truth_data[state]
            test = test_data[state]
            Column_titles = test[0]
            test.remove(test[0])
            test_data_frame = test.pop()
        
            for test_row in test_data_frame:
                    To_state = test_row[1]
                    for gndTruth_row in gnd_truth_frame:
                        if(To_state == gndTruth_row[1]):
                            diff = set(gndTruth_row).difference(set(test_row))
                        
                            if(len(diff) > 0):
                                diff = list(diff)
                                diff_data_to_report = []
                                for j in range(0,len(diff)):
                                    value_v2 = diff[j]
                                    id = gndTruth_row.index(value_v2)
                                    Column_title = (Column_titles[id-1]).replace("\n","")
                                    Column_title = Column_title.replace("info","")
                                    value_v3 = test_row[id]
                                    diff_data_to_report.append([value_v3,value_v2,Column_title])
                                mismatched_data.append([state,To_state,diff_data_to_report])


    report_path = os.path.join(path_to_reports_dir, 'MatrixElements_report.txt')
    # Display the mismatched data
    if(len(mismatched_data) > 0): 

        with open(report_path, 'w') as file: 
            file.write("\nFrom\tTo\t\t\tColumn\t\t\t\t\t\tValue in V3(Test)\t\t\tValue in V2(Ground Truth)")
            for mismatched_row in mismatched_data:
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
        file.write("No mismatched Data!!")

    return



def fetch_test_data_tables(driver,test_url,file_path):
     # load the web page
    driver.get(test_url)

    driver.implicitly_wait(20)

    num_clicks_on_More_states = 3

    MatrixElements_data_tables = {}

    # click on the "More stated" button to reveal more states
    while(num_clicks_on_More_states>0):

        btn_state_text = "//button[text()='More states']"
        
        try:
            More_states_btn = driver.find_element(By.XPATH, btn_state_text)
        except:
            return MatrixElements_data_tables


        More_states_btn.click()
        num_clicks_on_More_states = num_clicks_on_More_states - 1

    #Get all the buttons in the grid
    try:
        btns_grid = driver.find_element(By.XPATH,"//div[contains(@class, 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2')]")
    except:
        return MatrixElements_data_tables

    btns_grid_text = btns_grid.text

    displayed_btns_lst = list(btns_grid_text.split("\n"))
    analyzed_btns_states = []


    # Start clicking all the buttons and fetch the test data tables
    for btn in displayed_btns_lst:
        btn_chars = list((btn.split("/"))[0])
        btn_chars.pop()
        btn_state = ''
        for charac in btn_chars:
           btn_state = btn_state + charac
      
        if(btn_state not in analyzed_btns_states):
            btn_state_text = "//button[text()='" + btn_state + "']"
            try:
                buttons_list = driver.find_elements(By.XPATH, btn_state_text)
            except:
                print("An exception occurred")
                sys.exit()
            
            for btn in buttons_list:
                btn.click()

                #Reproduce the column titles first
                reproduced_titles = Reproduce_Column_titles(driver)
                #Reproduces the data in columns
                reproduced_data = Reproduce_Data(driver)

                MatrixElements_data_tables[btn.text] = [reproduced_titles,reproduced_data]
            
            analyzed_btns_states.append(btn_state)

    #Write fetch test tables to file  
    with open(file_path, 'w') as file: # saves modified html doc
        file.write(str(MatrixElements_data_tables))
    
    return MatrixElements_data_tables


def test_MatrixElementData(element,driver,gnd_truth_url,path_to_reports_dir):

    #Fetch the ground truth data
    gnd_truth_data_tables = Get_MatrixElements_data(element,gnd_truth_url)
    if(gnd_truth_data_tables == []):
        print("Ground Truth Data not available!!Property not tested...")
        return

     # Define the URL (Transition rates url for Li1)
    test_url = "https://www1.udel.edu/atom/dev/version3/matrix?element="+element


    # Set the path to the directory for the test file
    directory = os.getcwd() + '/Data/MatrixElements'

    test_file = element+'test'+'.txt'

    file_path = os.path.join(directory, test_file)

    test_data_tables = ''
    if(os.path.exists(file_path)):      # Needs to be removed going forward
        f = open(file_path)
        test_data_tables = f.read()
        test_data_tables = ast.literal_eval(test_data_tables)
    else:
        test_data_tables = fetch_test_data_tables(driver,test_url,file_path)
        if(test_data_tables == {}):
            print("Test Data not available!!Property not tested...")
            return
    
    Perform_Testing(gnd_truth_data_tables,test_data_tables,path_to_reports_dir)
    print("Test Complete!Report Generated...")
