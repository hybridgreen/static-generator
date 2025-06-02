import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_html_node(self):
        node1 = HTMLNode("div", None ,["p","a","h1"],None )
        node2 = HTMLNode("a","Link",None, {"href":"www.get_it.com", "target":"_blank"})
        
        #Tests
        self.assertEqual(node2.props_to_html(),  " href=\"www.get_it.com\" target=\"_blank\"")
        self.assertEqual(node1.props_to_html(), "")
        self.assertListEqual(node1.children, ["p","a","h1"])

        if __name__ == "__main__":
            unittest.main()