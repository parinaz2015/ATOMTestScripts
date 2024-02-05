

import sys,os

sys.path.append(os.getcwd()+'/fetch_Gnd_TRuth_Data')

import utils

data_type = 'Nuclear'

#0,3,4,5,6,9,12
def fetch_Nuclear_tables(atom,url):

    gndTruth_file = atom + 'Nuclear.html'
    url = url + gndTruth_file
    Nuclear_tables = utils.get_gnd_truth_tables(atom,url,data_type,'version2')

    return Nuclear_tables

def Get_Nuclear_data(atom,gnd_truth_url):

    gndTruth_Table = fetch_Nuclear_tables(atom,gnd_truth_url)
    if(gndTruth_Table == []):
        return gndTruth_Table

    for i in range(0,len(gndTruth_Table)):
        row = gndTruth_Table[i]
        row[0] = row[0].replace(" ", "")
        gndTruth_Table[i] = [row[0],row[3],row[4],row[5],row[6],row[9],row[12]]

    return gndTruth_Table