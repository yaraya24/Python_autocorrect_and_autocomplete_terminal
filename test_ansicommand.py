import unittest
from ansicommand import AnsiCommand

class TestCases(unittest.TestCase):
    test_case1 = AnsiCommand()
    
    

    def test_ansicommand(self):
        TestCases.test_case1.text = 'cd /home/user1'
        self.assertTrue(TestCases.test_case1.change_directory(), "Command that changes directory so needs to be True")
        TestCases.test_case1.text = 'cdd /home/user1'
        self.assertFalse(TestCases.test_case1.change_directory(), "Command doesn't change directory so False")
  



if __name__ == '__main__':
        unittest.main()