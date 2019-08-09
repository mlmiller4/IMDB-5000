import unittest
import IMDB
import pandas as pd

df = pd.read_csv("movie_metadata.csv")

class TestIMDB(unittest.TestCase):

    def test_calculateProfit(self):
        origNumCols = len(df.columns)
        result = IMDB.calculateProfit(df)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue('profit' in result.columns)     # check that 'profit' column exists

    def test_get_columns(self):
        result = IMDB.get_columns(df, ['genres','budget','gross'])
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result.columns), 3)
        self.assertTrue('genres' in result.columns and 'budget' in result.columns and 'gross' in result.columns)

        result = IMDB.get_columns(df,[])                # check case when no column names are specified
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result.columns), 0)

    def test_top_10_genres(self):
        result = IMDB.top_10_genres(df)
        self.assertIsInstance(result, pd.DataFrame)     # Check that results are a dataframe
        self.assertEqual(len(result), 10)       # Check that results have 10 values

        # Check if results are sorted in descending order
        tp = result['total_profit'].tolist()
        sort_tp = tp.copy()
        sort_tp.sort(reverse=True)
        self.assertEqual(tp, sort_tp)

    def test_top_10_actors(self):
        result = IMDB.top_10_actors(df)
        self.assertIsInstance(result, pd.DataFrame)     # Check that results are a dataframe
        self.assertEqual(len(result), 10)       # Check that results have 10 values

        # Check if results are sorted in descending order
        tp = result['total_profit'].tolist()
        sort_tp = tp.copy()
        sort_tp.sort(reverse=True)
        self.assertEqual(tp, sort_tp)

    def test_top_10_directors(self):
        result = IMDB.top_10_directors(df)
        self.assertIsInstance(result, pd.DataFrame)     # Check that results are a dataframe
        self.assertEqual(len(result), 10)       # Check that results have 10 values

        # Check if results are sorted in descending order
        tp = result['total_profit'].tolist()
        sort_tp = tp.copy()
        sort_tp.sort(reverse=True)
        self.assertEqual(tp, sort_tp)

    def test_top_10_pairs(self):
        result = IMDB.top_10_pairs(df)
        self.assertIsInstance(result, pd.DataFrame)     # Check that results are a dataframe
        self.assertEqual(len(result), 10)       # Check that results have 10 values

        # Check if results are sorted in descending order
        tp = result['total_profit'].tolist()
        sort_tp = tp.copy()
        sort_tp.sort(reverse=True)
        self.assertEqual(tp, sort_tp)

    def test_top_10_IMDB_pairs(self):
        result = IMDB.top_10_IMDB_pairs(df)
        self.assertIsInstance(result, pd.DataFrame)     # Check that results are a dataframe
        self.assertEqual(len(result), 10)       # Check that results have 10 values

        # Check if results are sorted in descending order
        tp = result['mean_IMDB_score'].tolist()
        sort_tp = tp.copy()
        sort_tp.sort(reverse=True)
        self.assertEqual(tp, sort_tp)


if __name__ == '__main__':
    unittest.main()
