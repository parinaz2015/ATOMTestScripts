

import sys,os

sys.path.append(os.getcwd()+'/fetch_Gnd_TRuth_Data')

import utils

data_type = 'MatrixElements'

def fetch_MatrixElements_tables(atom,url):
     
    gnd_truth_file = atom+".html"
    url = url+gnd_truth_file
    TR_tables_gnd_truth = utils.get_gnd_truth_tables(atom,url,data_type,'version2')
    return TR_tables_gnd_truth


def Get_MatrixElements_data(atom,gnd_truth_url):

    #Start by fetching the ground truth tables a.k.a tables from version 2
    ME_table_gnd_truth = fetch_MatrixElements_tables(atom,gnd_truth_url)
    if(ME_table_gnd_truth == []):
        return ME_table_gnd_truth
    ME_table_gnd_truth = utils.preprocess(ME_table_gnd_truth,data_type)

    #Get the ground truth buttons
    buttons_gnd_truth = ME_table_gnd_truth[0]
    buttons_gnd_truth = buttons_gnd_truth[1:]

    #Remove unnecessary spaces within button/state names
    states_list = []
    for btn_row in buttons_gnd_truth:
        if(len(btn_row)>1):
            for btn in btn_row:
                if((btn != '') and (btn not in states_list)):
                    states_list.append(btn.replace(" ", ""))

    #Populate the actual ground truth data
    #The data is generated in the form of a dictionary
    Actual_gnd_truth_data = ME_table_gnd_truth[1]
    gnd_truth_data_tables = {}

    for state in states_list:
        data = []
        for row in Actual_gnd_truth_data:
            if(row[0] == state):
                temp_row = [row[0],row[1],row[4],row[7]]
                data.append(temp_row)
        gnd_truth_data_tables[state] = data
   
    return gnd_truth_data_tables
  