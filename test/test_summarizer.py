import sys
sys.path.append('/h/172/howardchen/AutoFinViz/')

import unittest
import pandas as pd
from autofinviz.components.summarizer import Summarizer

class TestColsInfo(unittest.TestCase):

    def setUp(self):
        self.test_class_instance = Summarizer()

    def test_numeric_columns(self):
        df = pd.DataFrame({
            'int_col': [1, 2, 3],
            'float_col': [1.1, 2.2, 3.3]
        })
        result = self.test_class_instance.cols_info(df)
        expected_dtypes = ['number', 'number']
        for col, dtype in zip(result, expected_dtypes):
            self.assertEqual(col['properties']['dtype'], dtype)

    def test_boolean_column(self):
        df = pd.DataFrame({'bool_col': [True, False, True]})
        result = self.test_class_instance.cols_info(df)
        self.assertEqual(result[0]['properties']['dtype'], 'boolean')

    def test_string_column(self):
        df = pd.DataFrame({'str_col': ['a', 'b', 'c']})
        result = self.test_class_instance.cols_info(df)
        self.assertEqual(result[0]['properties']['dtype'], 'string')

    def test_date_column(self):
        df = pd.DataFrame({'date_col': pd.to_datetime(['2021-01-01', '2021-01-02', '2021-01-03'])})
        result = self.test_class_instance.cols_info(df)
        self.assertEqual(result[0]['properties']['dtype'], 'date')

    def test_categorical_column(self):
        df = pd.DataFrame({'cat_col': pd.Categorical(['a', 'b', 'a'])})
        result = self.test_class_instance.cols_info(df)
        self.assertEqual(result[0]['properties']['dtype'], 'category')


if __name__ == '__main__':
    unittest.main()