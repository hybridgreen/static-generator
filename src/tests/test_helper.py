import unittest
from textnode import *
from helper import *

class TestHelper(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(),"This is a text node")
    
    def text_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.to_html(),"<b>This is a bold node</b>")

    def test_text_italic(self):
        node = TextNode("Italicized text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italicized text")
        self.assertEqual(html_node.to_html(), "<i>Italicized text</i>")

    def test_text_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.to_html(), "<code>print('hello')</code>")

    def test_text_link(self):
        node = TextNode("OpenAI", TextType.LINK, "https://openai.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "OpenAI")
        self.assertEqual(html_node.to_html(), '<a href="https://openai.com">OpenAI</a>')

    def test_text_img(self):
        node = TextNode("A cute cat", TextType.IMG, "cat.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), '<img src="cat.jpg" alt="A cute cat">')

    def test_invalid_text_type(self):
        class UnknownType:
            pass
        node = TextNode("???", UnknownType())
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertIn("Invalid text node type", str(context.exception))

    def test_split_nodes_delimiter(self):
        expected_output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,expected_output)

        with self.assertRaises(Exception) as context:
            node = TextNode("This is text with **Bold words", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        self.assertIn("Invalid delimiter number, please check your syntax", str(context.exception))

        with self.assertRaises(Exception) as context:
            node = TextNode("This is text with **Bold words", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "", TextType.ITALIC)
        self.assertIn("Invalid text type or delimiter", str(context.exception))
