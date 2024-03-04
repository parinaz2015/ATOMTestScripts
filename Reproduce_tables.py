
from selenium.webdriver.common.by import By
import zipfile,glob
import webbrowser,shutil,os
import time, csv
import zipfile
import shutil
import glob
import time
from flask import Flask, render_template, send_file
from selenium import webdriver

#Function to scrape table column titles from the HTML
def Reproduce_Column_titles(driver):
    reproduced_titles = []
    try:
        column_titles = driver.find_elements(By.TAG_NAME, "th")
    except:
        return reproduced_titles
    
    if(len(column_titles)>0):
        for title in column_titles:
            reproduced_titles.append(title.text)
    return reproduced_titles

#Function to scrape the data within table columns from the HTML
def Reproduce_Data(driver):
    reproduced_data = []
    try:
        rows = driver.find_elements(By.TAG_NAME, "tr")
    except:
        return reproduced_data
    
    for row in rows:
    #print ii.tag_name
        cols = row.find_elements(By.TAG_NAME, "td")
        row_data = []
        if(len(cols) > 0):
            for entry in cols:
                row_data.append(entry.text)
            reproduced_data.append(row_data)

    return reproduced_data


#Atomic data tables reproduced in a different way (A better routine than the above two routines)
# TODO: Replace above two routines with this routine for all element properties.

def Get_Atomic_Test_Data(driver):

    Reproduced_tables = []
    WebElement_tables_list = []

    try:
       WebElement_tables_list = driver.find_elements(By.XPATH,"//table[contains(@class, 'table-auto text-center')]")
    except:
        return WebElement_tables_list
    
    # Going through each table element and reproducing the table from the element
    for WebElement_table in WebElement_tables_list:
   
        #Table header web element
        table_head = WebElement_table.find_element(By.TAG_NAME,"thead")

        table_WebElement_Column_titles = table_head.find_elements(By.TAG_NAME, "th")

        table_body = WebElement_table.find_element(By.TAG_NAME,"tbody")

        #Reproducing table column titles
        table_Column_titles = []
        for WebElement in table_WebElement_Column_titles:
            table_Column_titles.append((WebElement.text).replace("\n","").replace("Ref",""))


        #Reproducing table data from each Web element row
        table_WebElement_rows = table_body.find_elements(By.TAG_NAME, "tr")
        table_data = []
        for WebElement_row in table_WebElement_rows:
            #Getting the entries in each row
            Entries_WebElement = WebElement_row.find_elements(By.TAG_NAME, "td")
            
            row_data = []
            if(len(Entries_WebElement)>0):
                #Saving each entry
                for entry in Entries_WebElement:
                    row_data.append(entry.text)

                table_data.append(row_data)

        #Putting the table together [Column titles,table Data]
        table_data.insert(0,table_Column_titles)
        Reproduced_tables.append(table_data)

    return Reproduced_tables


#Fetches the test data for testing polarizability. The test data here is
# the Version 3 downloaded data.
def Get_Polarizability_Test_Data(driver,url,data_directory,element):
#  This function retrieves polarizability test data for a given chemical element from a specified URL.

#   Parameters:
#       - driver: Selenium webdriver object for browser automation.
#       - url: URL of the web page containing polarizability test data.
#       - data_directory: Directory to store downloaded and extracted data files.   
#       - element: Chemical element for which polarizability data is being retrieved.

#   Returns:
#       - test_table_dictionary: A dictionary containing polarizability test data organized by states.
#   Note:
#       - The function interacts with the web page to download a zip file containing CSV files,
#         extracts the files, and organizes the data into a dictionary.
    driver = webdriver.Chrome() 
    # load the web page
    driver.get(url)

    driver.implicitly_wait(10)
     # Find the "Download plotted data" button and click it
    try:
        # Click on all the checkboxes on the screen
        checkboxes = driver.find_elements(By.XPATH, '//i[@class="fa fa-check"]')
        for checkbox in checkboxes:
            # Execute JavaScript to change the visibility style attribute to "visible"
            driver.execute_script("arguments[0].style.visibility = 'visible';", checkbox)
            # Call the toggleSelectedState function
            # Run JavaScript to print debug message when the element becomes visible
           # driver.execute_script("console.log('dbg: selected state:', arguments[0].checked);", checkbox)
    
        time.sleep(10)  # After making the checkboxes visible, add additional wait time to ensure that any potential JavaScript actions or events triggered by the visibility change have time to execute before clicking the download button
        download_button = driver.find_element(By.XPATH, '//a[contains(text(), "Download plotted data")]')
        download_button.click()
    except:
        driver.quit()
        return "Error: Button not found"
    
    # Wait for the download to complete
    time.sleep(5)  # Adjust as needed
    
    # Close the browser
    #driver.quit()

    # Find the downloaded file
    downloaded_files = glob.glob(os.path.join(os.path.expanduser('~'), 'Downloads', element+'DynamicPolarizabilities*.zip'))
    # Get a list of matching files
    #matching_files = glob.glob(pattern)

    # Find the most recently created file
    most_recent_file = max(downloaded_files, key=os.path.getctime)
    if len(downloaded_files) == 0:
        return "Error: Downloaded file not found"
    
    # Get the path to the downloaded file
    downloaded_file_path = most_recent_file #downloaded_files[0]
    
    # Move the downloaded file to the destination folder
    #C:\Users\parin\Desktop\Atom\ATOM-testing\Data\Polarizability\Li1\Test
    shutil.move(downloaded_file_path, data_directory)

    # Unzip the file
    with zipfile.ZipFile(os.path.join(data_directory, os.path.basename(downloaded_file_path)), 'r') as zip_ref:
        zip_ref.extractall(data_directory)
        
    # Remove the zip file
    os.remove(os.path.join(data_directory, os.path.basename(downloaded_file_path)))

    # Dictionary to store polarizability test data
    test_table_dictionary = {}

    WebElement = ''


    #List all the extracted CSV files
    csv_files = glob.glob(data_directory + '*.csv')
    # Process each CSV file and organize data into the dictionary
    for file_path in csv_files:
        with open(file_path, mode ='r')as file:
            file_content = list(csv.reader(file))

# this part needs to be modified so that similar file names are stored.
            #string_with_state = (file_path.split("2p_"))[1] 
            # Extract state information from the file path
        # if "2s_" in file_path:
        #     string_with_state = file_path.split("2s_")[1]
        # elif "2p_" in file_path:
        #     string_with_state = file_path.split("2p_")[1]
        # elif element + "_" in file_path:
        #     string_with_state = file_path.split(element + "_")[1]
        # else:
        #     print("Error: Invalid file name format")
        #     continue  # Skip this file and move to the next one
            #state_string = (string_with_state.split("_Dynamic_"))[0]
        string_with_state = os.path.basename(file_path)
        state = (string_with_state.split(".csv"))[0] #.replace("_","").replace("-2","")

            #header = file_content[0]
            #state = header[1]
            # file_content.remove(header)
         # Convert state to lowercase
        state = state.lower()
        test_table_dictionary[state] = file_content

    for state, data_table in test_table_dictionary.items():
    # Print the name of the table (state)
        print("Table Name:", state)
    
    # Print the first row of the table
        if data_table:
            print("First Row:", data_table[0])
        else:
            print("Table is empty")    
    # Return the dictionary containing polarizability test data
    return test_table_dictionary


