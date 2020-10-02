import unittest
from auto_complete_trie import PrefixTree
import config

class TestCases(unittest.TestCase):
    config.list_of_commands = PrefixTree.read_all_commands()
    test_case1 = PrefixTree()
    test_case1.insert('python3 main.py')
    test_case1.insert('cd home/user1')
    test_case1.insert('ls -la')
    test_case1.insert('ls -las')
    test_case1.insert('cd home/user2')


    def test_autocomplete(self):
        self.assertIsNot(TestCases.test_case1.search_trie('python3 main.py'), False, "Shouldn't be False")
        self.assertFalse(TestCases.test_case1.search_trie('python3'), "Should be False as word not in command")
        self.assertIsNot(TestCases.test_case1.search_trie('cd home/user1'), False, "Shouldn't be False")
        self.assertIsNot(TestCases.test_case1.search_trie('ls -la'), False, "Shouldn't be False")
        self.assertFalse(TestCases.test_case1.search_trie('ls /la'), "Should be False as word not in command")

        self.assertEqual(TestCases.test_case1.auto_complete('ls'), ['ls -la', 'ls -las'], "Should return the lists")
        self.assertEqual(TestCases.test_case1.auto_complete('cd'), ['cd home/user1', 'cd home/user2'], "Should return the lists")
        self.assertEqual(TestCases.test_case1.auto_complete('cd home/user1'), ['cd home/user1'], "Should return the lists")
        self.assertEqual(TestCases.test_case1.auto_complete('cd home/user'), ['cd home/user1', 'cd home/user2'], "Should return the lists")
        self.assertEqual(TestCases.test_case1.auto_complete('cd home/account'), [], "Should return empty list")
        self.assertEqual(TestCases.test_case1.auto_complete('python2'), [], "Should return empty list")

        self.assertEqual(config.list_of_commands[0], 'clear', 'First command should be clear')

        

if __name__ == '__main__':
    unittest.main()