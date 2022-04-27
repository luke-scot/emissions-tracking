
"""Import classes for each type of LCA and chemical manufacturing data used in emissions-tracking project"""

import numpy as np
import pandas as pd


class LCA(object):
    """Import EcoInvent CO2e data"""
    def __init__(self, data_path:str, lca_lists:list):
        self.data = pd.DataFrame()
        for path in lca_lists:
            filepath = data_path+"EcoInvent/"+path+"/GWP100a_IPCC2013.csv"
            try:
                raw = pd.read_csv(filepath)
            except FileNotFoundError:
                print(filepath+' not found')
                raise
            self.data = self.data.append(raw[['name', 'location', 'CO2e']][~raw['generalComment'].str.contains('market')].sort_values('name'))
        self.data_path = data_path

    def location(self, location='Global'):
        """Filter entries for EcoInvent regions"""
        loc_filepath = self.data_path+"EcoInvent/EcoInvent_locations.csv"
        loc_codes = pd.read_csv(loc_filepath)
        region_code = loc_codes['Code'][np.where(loc_codes['Name'] == location)[0]].iloc[0]
        rows = []
        for product in self.data['name'].unique():
            for code in [region_code, 'RoW', 'GLO']:
                found = self.data[(self.data['name']==product) & (self.data['location']==code)]
                if not found.index.empty:
                    rows += list(found.index)
                    break
        return self.data.loc[rows].groupby(['name','location']).mean().reset_index()


class IHSData(object):
    """Import IHS Markit chemical product and material composition data"""
    def __init__(self, data_path):
        product_file = data_path+"IHS/US/products.csv"
        material_file = data_path+"IHS/US/materials.csv"
        self.products = pd.read_csv(product_file, index_col=0).reset_index(drop=True)
        self.materials = pd.read_csv(material_file, index_col=0).reset_index(drop=True)


class ICISData(object):
    """Import ICIS chemical manufacturing data"""
    def __init__(self, filepath):
        self.countryCol = 'COUNTRY/TERRITORY'
        self.properties = ['Capacity', 'Statistic Production', 'Import', 'Export', 'Consumption']
        in_file = pd.ExcelFile(filepath)
        self.plants, self.prod, self.imps, self.exps, self.cons = [pd.DataFrame()]*5

        def append_data(prev,region,breaks,start):
            """Append data while row of ICIS data is within particular type"""
            br_end = breaks[start+1] if start+1 < len(breaks) else -1
            return prev.append(region[breaks[start]+1:br_end].dropna(subset=[self.countryCol]), ignore_index=True)

        for sheet in in_file.sheet_names[2:]:
            region = pd.read_excel(in_file, sheet_name=sheet)
            region['Region'] = [sheet]*len(region)
            breaks = region.loc[region['PRODUCT'].isin(self.properties)].index
            self.plants, self.prod, self.imps, self.exps, self.cons = [append_data(attr,region,breaks,i)
                                                                       for i, attr in enumerate([self.plants, self.prod, self.imps, self.exps, self.cons])]
