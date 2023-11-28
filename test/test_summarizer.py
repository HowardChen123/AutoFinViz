import sys
sys.path.append('/h/172/howardchen/AutoFinViz/')

import unittest
import pandas as pd
from autofinviz.components.summarizer import Summarizer

class TestColsInfo(unittest.TestCase):

    def setUp(self):
        self.test_class_instance = Summarizer()

    def test_column_types(self):
        df = pd.DataFrame({
            'int_col': [1, 2, 3],
            'float_col': [1.1, 2.2, 3.3],
            'bool_col': [True, False, True],
            'str_col': ['a', 'b', 'c'],
            'date_col': pd.to_datetime(['2021-01-01', '2021-01-02', '2021-01-03']),
            'cat_col': pd.Categorical(['a', 'b', 'a'])
        })

        result = self.test_class_instance.cols_info(df)
        expected_dtypes = ['number', 'number', 'boolean', 'string', 'date', 'category']

        for col, expected_dtype in zip(result, expected_dtypes):
            self.assertEqual(col['properties']['dtype'], expected_dtype)


if __name__ == '__main__':
    unittest.main()