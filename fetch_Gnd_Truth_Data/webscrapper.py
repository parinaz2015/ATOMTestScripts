
import os
import requests
from bs4 import BeautifulSoup


# for parsing all the tables present
# on the websites
from html_table_parser.parser import HTMLTableParser

def static_page_scrapper(atom,url, gnd_truth_version,data_type): 
    
    html_file = atom + '_GndTruth' + '_' + gnd_truth_version +'.html'  
    directory = os.getcwd() + '/Data/'+data_type

    file_path = os.path.join(directory, html_file)
    # if(os.path.exists(html_file)):
    #     return html_file
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    with open(file_path, 'wb') as file: # saves modified html doc
        file.write(soup.prettify('utf-8'))
    response.close()

    return file_path


def get_html_feed(html_file):
    f = open(html_file,"r")

    xhtml = f.read()
    
    # Defining the HTMLTableParser object
    p = HTMLTableParser()
    
    # feeding the html contents in the
    # HTMLTableParser object
    p.feed(xhtml)

    return p
