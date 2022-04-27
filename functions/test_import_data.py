
"""Unit tests for import_data.py"""

import unittest
import pandas as pd
import functions.import_data as id


class LCATests(unittest.TestCase):
    def test_LCA_import(self):
        valid_data = id.LCA("C:/Users/lshc3/Documents/", ['Basic_chemicals_201','Coke_Petro_19']).data
        self.assertIsInstance(valid_data, pd.DataFrame, 'Import does not return valid pandas Dataframe')
        self.assertAlmostEqual(valid_data['CO2e'][0], 4.86288208344407, 3, msg = 'Incorrect value found on test case')
        self.assertRaises(FileNotFoundError, lambda: id.LCA("C:/Users/lshc3/Documents/", ['invalid list']))

    def test_LCA_location(self):
        filt_locs = id.LCA("C:/Users/lshc3/Documents/", ['Basic_chemicals_201','Coke_Petro_19']).location('France')
        print(set(filt_locs['location']))
        self.assertTrue(set(filt_locs['location']).issubset(['GLO','RoW','FR']), 'Location filter returns unwanted locations')

class IHSDataTests(unittest.TestCase):
    def test_products(self):
        self.assertIsInstance(id.IHSData("C:/Users/lshc3/Documents/").products, pd.DataFrame, 'Import does not return valid pandas Dataframe')
        self.assertEqual(id.IHSData("C:/Users/lshc3/Documents/").products['Name'][0], 'ETHYLENE', 'Incorrect value found on test case')
    def test_materials(self):
        self.assertIsInstance(id.IHSData("C:/Users/lshc3/Documents/").materials, pd.DataFrame, 'Import does not return valid pandas Dataframe')
        self.assertEqual(id.IHSData("C:/Users/lshc3/Documents/").materials['Source'][0], 'CATALYST', 'Incorrect value found on test case')

# class IHSDataTests(unittest.TestCase):
#     def test_dataframes(self):
#         icis = id.ICISData("C:/ICIS_data/US_allchemicals.xlsx")
#         #for i in [icis.plants, icis.prod, icis.imps, icis.exps, icis.cons]:
#         self.assertIsInstance(icis.plants, pd.DataFrame, 'Import does not return valid pandas Dataframe')
#         self.assertIsInstance(icis.prod, pd.DataFrame, 'Import does not return valid pandas Dataframe')

if __name__ == '__main__':
    unittest.main()
