import unittest
import time
from spellcheck import spellcheck_API
import config

class TestCases(unittest.TestCase):
    config.dictionary_list = spellcheck_API.read_dictionary_text()
    test_instance1 = spellcheck_API('python')
    test_instance2 = spellcheck_API('pyton')
    test_instance3 = spellcheck_API('i am 10years old')
    test_instance4 = spellcheck_API('/pyton/adress/plese')
   

    def test_spelling(self):
        self.assertTrue(TestCases.test_instance1.check_dictionary(), "Should be True")
        self.assertEqual(TestCases.test_instance1.get_spellcheck(), '', "Should be empty as correctly spelt")
        self.assertIsNone(TestCases.test_instance2.check_dictionary(), "Should be None")
        time.sleep(1)                                                                                           #due to restrictions with Bing API calls, only allows 1 per second
        self.assertEqual(TestCases.test_instance2.get_spellcheck(), 'python', "Should return python")
        time.sleep(1)
        self.assertTrue(TestCases.test_instance3.check_dictionary(), "Should be True") 
        self.assertEqual(TestCases.test_instance3.get_spellcheck(), 'I am 10 years old', "Should capitalise and put spaces")
        time.sleep(1)
        self.assertEqual(TestCases.test_instance4.get_spellcheck(), '/python/address/please', "Should return /python/address/please")


if __name__ == '__main__':
    unittest.main()