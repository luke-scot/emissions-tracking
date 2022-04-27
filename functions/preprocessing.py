
"""Preprocessing functions for chemical data"""

import difflib
import pandas as pd

def format_icis(icis,year=2019):
    plants_clean = icis.plants.drop(columns=['#','DERIVATIVE','NOTE','@','@Sub','Region']+list(filter(lambda i: 'None' in str(i) or (type(i) is int and i!=year), icis.plants.columns)))
    plants_working = plants_clean[plants_clean[year] != '-'].reset_index(drop=True)
    return plants_working

def merge_chemical_data(lca, ihs, plants):
    """Add EcoInvent LCA data and IHS materials data to ICIS plant data dataframe"""
    merge = pd.merge(lca, plants, left_on=lca['name'].str.lower(), right_on=plants['PRODUCT'].str.lower(), how="left").reset_index(drop=True)
    plant_details = pd.merge(merge, ihs.materials, left_on=merge['PRODUCT'].str.lower(), right_on=ihs.materials['Product'].str.lower(), how="left")
    return plant_details

# def merge_ihs_icis(ihs, icis):
#     plants_working['ihsProcess'] = list(map(lambda x: next(iter(difflib.get_close_matches(str(x), ihs.products['Process'])),None), plants_working['PRODUCT']+' '+plants_working['ROUTE']+' '+plants_working['TECHNOLOGY']))
#     plant_products = pd.merge(plants_working, ihs, left_on=plants_working['ihsProcess'], right_on=ihs.products['Process'], how="left")
#     return plant_products

