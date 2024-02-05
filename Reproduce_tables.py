
from selenium.webdriver.common.by import By
import zipfile,glob
import webbrowser,shutil,os
import time, csv


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

    # load the web page
    driver.get(url)

    driver.implicitly_wait(10)
    # Dictionary to store polarizability test data
    test_table_dictionary = {}

    WebElement = ''

    # Find the Download CSV button and click it.
    try:
       WebElement = driver.find_element(By.XPATH,'//a[@href="'+"/atom/dev/version3/polarizability-files/Li1Pol.zip"+'"]')
    except:
        return test_table_dictionary ## If the element is not found, return an empty dictionary

    webbrowser.open(WebElement.get_attribute('href'))  # Open the download link in the web browser
  
    time.sleep(5)  

    # Download the zip folder and extract the CSV files.
    path_to_downloaded_zip_folder = data_directory + element + 'Pol.zip'
    path_to_extracted_files = data_directory + element + 'Pol/'

    # Extract the CSV files from the downloaded zip folder
    if(os.path.exists(path_to_extracted_files) == False):
        with zipfile.ZipFile(path_to_downloaded_zip_folder, 'r') as zip_ref:
            zip_ref.extractall(data_directory)


        #On MACOS, an extra folder __MACOSX is created after runnin the unzip command.
        #Remove this folder if present
        MACOSX_folder = data_directory + '/__MACOSX'
        if(os.path.exists(MACOSX_folder)):
            shutil.rmtree(MACOSX_folder)

    #List all the extracted CSV files
    csv_files = glob.glob(path_to_extracted_files + '*.csv')
    # Process each CSV file and organize data into the dictionary
    for file_path in csv_files:
        with open(file_path, mode ='r')as file:
            file_content = list(csv.reader(file))
            header = file_content[0]
            state = header[1]
            file_content.remove(header)
            test_table_dictionary[state] = file_content
    # Return the dictionary containing polarizability test data
    return test_table_dictionary
