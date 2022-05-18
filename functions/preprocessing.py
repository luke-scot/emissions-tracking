
"""Preprocessing functions for chemical data"""

import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz


def left_merge(df1, df2, col1, col2):
    return pd.merge(df1, df2, left_on=df1[col1].str.lower(), right_on=df2[col2].str.lower(), how="left").reset_index(drop=True).drop('key_0',axis=1)


def format_icis(icis,year=2019):
    plants_clean = icis.plants.drop(columns=['#','DERIVATIVE','NOTE','@','@Sub','Region']+list(filter(lambda i: 'None' in str(i) or (type(i) is int and i!=year), icis.plants.columns)))
    plants_working = plants_clean[plants_clean[year] != '-'].reset_index(drop=True)
    return plants_working


def merge_chemical_data(lca, ihs, plants):
    """Add EcoInvent LCA data and IHS materials data to ICIS plant data dataframe"""
    # LCA merge
    plants_lca = left_merge(plants, lca, 'PRODUCT', 'name')

    # IHS product merge
    plants_products = left_merge(plants_lca, ihs.products, 'name', 'Name')
    matches = [fuzz.ratio(str(i)+' '+str(j), str(k)) for i,j,k in zip(plants_products['ROUTE'], plants_products['TECHNOLOGY'], plants_products['Process'])]
    for i in np.where(plants_products['Process'] == 'NaN')[0]:
        matches[i] = 0
    plants_products['process_match'] = matches
    plants_products = plants_products.sort_values(list(plants_products.columns[:12])+['process_match']).drop_duplicates(plants_products.columns[:12],keep='last').reset_index(drop=True)
    plants_products.drop('process_match', axis=1, inplace=True)

    # IHS materials merge
    sparse_materials = ihs.materials[['Target','Source','Value','Source cost']].groupby(['Target','Source']).sum().unstack().reset_index()
    plants_materials = left_merge(plants_products, sparse_materials, 'Process', 'Target')
    return plants_materials
