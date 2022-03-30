#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

import annotate_position
import unittest

class TestCodingChallenge(unittest.TestCase):

    def setUp(self):
        """ Read in required dataframes for tests"""
        try:
            annotations_df = pd.read_csv('./unit_tests/test_annotations', sep='\t',
                                         names=['chr', 'refFlat', 'coding', 'start', 'end', 'score1', 'strand',
                                                'score2',
                                                'annotation', 'z'])
        except IOError:
            print 'cannot read annotations'


    def test_group_annotations(self):
        _series = pd.Series([134197558.0, 134201648.0, None, None])
        _series.name = "end"
        pd.testing.assert_series_equal(annotations_df['chr3'], _df)
        self.assertEqual(annotate_position.group_annotations(annotations_df), _series)


if __name__ == "__main__":
    unittest.main()



