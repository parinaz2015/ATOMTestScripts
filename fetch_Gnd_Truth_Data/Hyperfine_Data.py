


import sys,os

sys.path.append(os.getcwd()+'/fetch_Gnd_TRuth_Data')

import utils

data_type = 'Hyperfine'

def fetch_Hyperfine_tables(atom,url):
     
    gnd_truth_file = atom+"Hyperfine.html"
    url = url+gnd_truth_file
    TR_tables_gnd_truth = utils.get_gnd_truth_tables(atom,url,data_type,'version2')
    return TR_tables_gnd_truth


def Get_Hyperfine_data(atom,gnd_truth_url):

    gndTruth_Table = fetch_Hyperfine_tables(atom,gnd_truth_url)
    if(gndTruth_Table == []):
        return [],[]

    gndTruth_Table_Columns = gndTruth_Table[0]

    gndTruth_Table_Data = gndTruth_Table[1:]


    #0,1,2,4
    for i in range(0,len(gndTruth_Table_Data)):
        row = gndTruth_Table_Data[i]
        row[1] = row[1].replace(" ", "")
        if(row[4] != ''):
            row[4] = row[4].replace(" Ref", "")
    
        if(row[2] != '' ):
            row[2] = row[2].replace(" Ref", "")


        gndTruth_Table_Data[i] = [row[0],row[1],row[2],row[4]]

    gndTruth_Table_Columns = [gndTruth_Table_Columns[0],gndTruth_Table_Columns[1],gndTruth_Table_Columns[2],gndTruth_Table_Columns[4]]

    return gndTruth_Table_Columns, gndTruth_Table_Data