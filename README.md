# ATOM Website Testing

This README provides instructions on how to run the scripts to test
Version 3 against Version 2 of the website. Details about the 
various directories has also been provided.

Access File to Atom Project: https://docs.google.com/document/d/1snUMKd2w-gYzlHpy08NvHaffJXlJNfV5NPAVtRyAQUQ/edit?usp=sharing

Version 2 - https://www1.udel.edu/atom/index.html

Version 3 - https://www1.udel.edu/atom/dev/version3/
- Frontend: https://github.com/amanikiruga/atom-v3 
- Backend: https://github.com/amanikiruga/atomv3-backend 
- Testing v2.0: https://github.com/parinaz2015/ATOMTestScripts

## Dependencies

1. Software level\
(a) Python 3.7 and above\
(b) Google Chrome

2. Python packages\
(a) Selenium\
(b) bs4\
(c) requests\
(d) html_table_parser\
(e) webdriver_manager\
(f) html-table-parser-python3\
(g) numpy

## Directory Structure

Directories and what they contain:
1. Data - Stores all the downloaded data (Ground truth and Test)
          according to the properties

2. fetch_Gnd_Truth_Data - Contains scripts for fetching the
                        ground truth data

3. test_scripts - Contains scripts that perform the actual testing
                      for each property

4. reports - The generated reports for each element

5. root directory - Contains the master script and some utility scripts

## Installing Python packages

Install the required python packages using pip or pip3 package manager,
Using the command:


    pip3 install -r requirements.txt

Note: A package that is not listed but requried is "BeautifulSoup4".
The reason it is not listed is that installing through the text file
creates issues which are yet to be understood (possibly conflicts with the pacakge
html_table_parser). Install this package after installing the packages within
requirements.txt as follows:

    pip3 install bs4

## Running the scripts and testing

The master script is the "dynamic_scrape_and_test.py" script. Run this script
using the following command: 
   
    For Macintosh: python3 dynamic_scrape_and_test.py
    For Windows:   python -Xutf8 dynamic_scrape_and_test.py

Notes:
1. Data for all properties are tested for all elements.

2. The ground truth and test data for properties such as Transition Rates and Matrix Elements 
    is downloaded and placed in the "Data" directory. This is just to save time for testing of these
    properties. Going forward every run of the master script will open the ground
    truth and test websites and download the requried data.

## Generation of Test Reports

Test reports are generated when the master script is executed. 
The generated reports are placed in the reports->*element_name* directory. The naming
convention used for the reports is *property*_report.txt.

## Constraints

1. Data for a number of elements is not yet available for testing.
2. If the number of rows and columns in a data table do not match, 
   no testing is performed for the table.
3. Rows of Test and Ground truth tables are matched. It is a string
   match because of the way data is displayed on the website.
