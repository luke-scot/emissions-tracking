
import unittest
# import sys
# sys.path.append('C:/Users\lshc3\PycharmProjects\emissions-tracking')
# from functions.importData import LCA, IHSData, ICISData
import functions.import_data as id

class LCATest(unittest.TestCase):

        #self.valid_data =

    def test_true(self):
        # print(utl.to_listlist(['listyy']))
        # self.assertEqual(utl.to_listlist(['listyy']),utl.to_listlist(['listyy']))
        #self.assertEqual(,True)
        valid_data = id.LCA("C:/Users/lshc3/Documents/", ['Test_chemicals'])
        self.assertEqual(valid_data[0]['CO2e'], 4.86288208344407, 'Incorrect value found on test case')
        #self.assertIsInstance(id.LCA("C:/Users/lshc3/Documents/", ['Test_chemicals']), pd.DataFrame(), 'Import does not return valid pandas Dataframe')
        self.assertEqual(True,False)

    # def valid_import(self):
    #     self.assertIsInstance(self.valid_data, pd.DataFrame, 'Import does not return valid pandas Dataframe')
    #     self.assertEqual(self.valid_data[0]['CO2e'], 4.86288208344407, 'Incorrect value found on test case')
    #     self.assertRaises(FileNotFoundError, lambda: ipdata.LCA("C:/Users/lshc3/Documents/", ['invalid list']),
    #                       msg='FileNotFound error not raised for invalid filepath')
    #
    # def location_filter(self):
    #     filt_locs = set(self.valid_data.location('USA')['location'])
    #     self.assertTrue(filt_locs.issubset(['GLO','RoW','USA']), 'Location filter returns unwanted locations')

# class IHSData_test(unittest.TestCase):
#     def valid_products(self):
#         self.assertEqual(True, False, 'Invalid product read')
#     def valid_materials(self):
#         self.assertEqual(True,False, )

if __name__ == '__main__':
    unittest.main()

