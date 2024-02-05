



import sys,os,re

sys.path.append(os.getcwd()+'/fetch_Gnd_TRuth_Data')

import utils

data_type = 'Atomic'


#Actual fetching routine
def fetch_Atomic_tables(atom,url):

    gndTruth_file = atom + 'hci.html'
    url = url + gndTruth_file
    Energies_Table,TREnergies_Table = utils.get_gnd_truth_tables(atom,url,data_type,'version2')

    return Energies_Table,TREnergies_Table


#The ground truth table has latex characters. These characters need to be removed.
def table_cleanup(table):
    Modified_gndTruth_Table = []

    for i in range(0,len(table)):
        temp_row = table[i]
        exclude = '\\'

        for i in range(0,len(temp_row)):

            temp_row[i] = re.sub('[{$_}]', '', temp_row[i])

            temp_row[i] = re.sub("times", '', temp_row[i])

            temp_row[i] = re.sub("Ref", '', temp_row[i])

            temp_row[i] = ''.join(ch for ch in temp_row[i] if ch not in exclude)

        Modified_gndTruth_Table.append(temp_row)

    #Modified_gndTruth_Table[2:] is temporary and should be changed.
    #This special casing is because of the separate row of units in the ground truth table.
    Modified_gndTruth_Table = [Modified_gndTruth_Table[0],Modified_gndTruth_Table[2:]]

    return Modified_gndTruth_Table


#Get the atomic data tables
def Get_Atomic_data(atom,gnd_truth_url):

    gndTruth_Table1,gndTruth_Table2 = fetch_Atomic_tables(atom,gnd_truth_url)

    if(gndTruth_Table1 == [] and gndTruth_Table2 == []):
        return []

    #Remove unwanted and problematic latex characters the tables
    gndTruth_Table1 = table_cleanup(gndTruth_Table1)

    if(gndTruth_Table2 != []):    
        gndTruth_Table2 = table_cleanup(gndTruth_Table2)

    return [gndTruth_Table1, gndTruth_Table2]

#Get the atomic data tables
def Get_GndTruth_Atomic_data(atom,gnd_truth_url):

    gndTruth_Table1,gndTruth_Table2 = fetch_Atomic_tables(atom,gnd_truth_url)

    if(gndTruth_Table1 == [] and gndTruth_Table2 == []):
        return []

    #Remove unwanted and problematic latex characters the tables
    gndTruth_Table1 = table_cleanup(gndTruth_Table1)

    if(gndTruth_Table2 != []):    
        gndTruth_Table2 = table_cleanup(gndTruth_Table2)

    return [gndTruth_Table1, gndTruth_Table2]