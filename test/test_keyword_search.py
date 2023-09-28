# coding: utf-8

# 標準モジュール
import os
import sys
import unittest

# 外部モジュール

# 内部モジュール
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './..')))
from keyword_search import KeywordSearch


class TestKeywordSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        begin all tests
        :return:
        """
        cls.obj = KeywordSearch()

    @classmethod
    def tearDownClass(cls):
        """End all tests"""
        pass

    def setUp(self):
        """Begin each test"""
        pass

    def tearDown(self):
        """Start each test"""
        pass

    def execute_test(self, test_func, test_param):
        """
        テスト実行共通関数
        Calling::
            obj.execute_test(
                test_func,       (i) test function
                test_param,      (i) test param
            )
        Returns::
            - errmsg (unicode)   : error msg
        Details::
        """
        raise_flg = test_param['raise']
        in_params = test_param['IN']
        if 'OUT' in test_param:
            out_params = test_param['OUT']
        else:
            out_params = None

        print_msg = 'func = {}; in = {}; out = {}; raise = {}'
        print_msg = print_msg.format(test_func.__name__, in_params, out_params, raise_flg)
        print(print_msg)

        if raise_flg is True:
            with self.assertRaises(Exception) as ex:
                test_func(**in_params)
            print('test errmsg: {}'.format(ex.exception))
            errmsg = 'exception.message : {}'.format(ex.exception)
            self.assertTrue(errmsg.find(out_params) > -1)

            return None
        else:
            result = test_func(**in_params)
            if out_params is not None:
                self.assertEqual(result[:-1], out_params[:-1])

            return result

    def test_run(self):
        """
        test run
        :return:
        """
        print('test run')

        test_func = self.obj.run

        test_params = (
            {'raise': False,
             'IN': {},
             'OUT': None},
        )

        for test_param in test_params:
            result = self.execute_test(test_func, test_param)
            
    def test_search_keywords_in_lines(self):
        """
        test search_keywords_in_lines
        :return:
        """
        print('test search_keywords_in_lines')

        test_func = self.obj._search_keywords_in_lines

        lines = None
        with open('app_20230912.log', 'r') as f:
            lines = f.readlines()
        
        test_params = (
            {'raise': False,
             'IN': {'lines': lines, 'file': 'app_20230912.log'},
             'OUT': None},
        )

        for test_param in test_params:
            result = self.execute_test(test_func, test_param)
            self.assertEqual(len(result), 21)

if __name__ == '__main__':
    unittest.main(failfast=True)
