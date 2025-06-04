import unittest
import main

class Test_main(unittest.TestCase):
    def test_extract_title(self):
        title = main.extract_title("# Hello World")
        self.assertEqual("Hello World",title)
        with self.assertRaises(Exception) as context:
            main.extract_title("#Hello World")
        self.assertEqual(str(context.exception), "Invalid markdown- Page must have a # Title")
        
    if __name__ == "__main__":
        unittest.main()