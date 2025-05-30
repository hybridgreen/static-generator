import unittest

from leafnode import *

class TestLeaf(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        test_props = {
            "href":"www.goat.se",
            "type":"this is bogus"
        }

        node2 = LeafNode("a","Click Me!",test_props)
        print(node2)

        self.assertEqual(node2.to_html(), "<a href=\"www.goat.se\" type=\"this is bogus\">Click Me!</a>")
        
        with self.assertRaises(ValueError) as context:
            node3 = LeafNode(None,None,test_props)

        self.assertEqual(str(context.exception),"All nodes must have a value")
    
    if __name__ == "__main__":
        unittest.main()