
"""Script for running graph classification on chemical data"""

import functions.import_data as impData
import functions.preprocessing as preproc

# Import data
data_path = "C:/Users/lshc3/Documents/"
lca = impData.LCA(data_path, lca_lists = ['Basic_chemicals_201','Coke_Petro_19']).location('United States')
ihs = impData.IHSData(data_path)
icis = impData.ICISData("C:\ICIS_data/US_allchemicals.xlsx")

# Merge data
plants = preproc.format_icis(icis, 2019)
merged_data = preproc.merge_chemical_data(lca,ihs,plants)

