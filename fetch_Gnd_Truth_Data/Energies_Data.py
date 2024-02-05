

import sys,os

sys.path.append(os.getcwd()+'/fetch_Gnd_TRuth_Data')

import utils

data_type = 'Energies'

#0,3,4,5,6,9,12
def fetch_Energies_tables(atom,url):

    gndTruth_file = atom + 'Energies.html'
    url = url + gndTruth_file
    Energies_tables = utils.get_gnd_truth_tables(atom,url,data_type,'version2')

    return Energies_tables

def Get_Energies_data(atom,gnd_truth_url):

    gndTruth_Table = fetch_Energies_tables(atom,gnd_truth_url)

    if(gndTruth_Table == []):
        return gndTruth_Table

    Modified_gndTruth_Table = []
    for i in range(0,len(gndTruth_Table)):
        row = gndTruth_Table[i]
        if(len(row)>2):
            break
        row[0] = row[0].replace(" ","")
        Modified_gndTruth_Table.append(row)

    return Modified_gndTruth_Table