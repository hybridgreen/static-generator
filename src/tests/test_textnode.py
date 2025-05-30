import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_ed(self):
        node = TextNode("This is the first node", TextType.BOLD)
        node2 = TextNode("This is the second node", TextType.BOLD)
        node3 = TextNode("This is the first node", TextType.BOLD)
        linknode = TextNode("This is the first node", TextType.LINK, "www.get_it.com")
        self.assertNotEqual(node, node2)
        self.assertEqual(node, node3)
        self.assertNotEqual(node3,linknode)


    if __name__ == "__main__":
        unittest.main()