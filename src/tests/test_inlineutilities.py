import unittest
from textnode import *
from utility import *

class Test_Inline_utilities(unittest.TestCase):

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

    def test_extract_single_image(self):
        text = "Here is an image ![alt text](image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "image.png")])

    def test_extract_multiple_images(self):
        text = "![one](1.png) some text ![two](2.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("one", "1.png"), ("two", "2.png")])

    def test_image_with_empty_alt(self):
        text = "Check this ![](img.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("", "img.png")])

    def test_image_with_empty_url(self):
        text = "Broken image ![logo]()"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("logo", "")])

    def test_image_nested_brackets(self):
        text = "Example ![complex [alt]](complex.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("complex [alt]", "complex.png")])

    def test_image_no_match_on_text(self):
        text = "This is just text (not markdown)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_image_malformed(self):
        text = "Broken ![alt](missing"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    # ----------- LINKS ------------

    def test_extract_single_link(self):
        text = "Click [here](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("here", "https://example.com")])

    def test_extract_multiple_links(self):
        text = "[One](1.com) and [Two](2.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("One", "1.com"), ("Two", "2.com")])

    def test_link_with_empty_text(self):
        text = "[](/empty-text)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("", "/empty-text")])

    def test_link_with_empty_url(self):
        text = "[text]()"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("text", "")])

    def test_link_nested_brackets(self):
        text = "[A [B]](nested.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("A [B]", "nested.com")])

    def test_link_ignores_image(self):
        text = "Image ![alt](img.png) and [link](link.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "link.com")])

    def test_link_malformed(self):
        text = "Broken [link](missing"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

# -------------- Split Images and Links -------------

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png")
        ],
        new_nodes
        )

    def test_split_link(self):
        node = TextNode(
        "This is text with a link [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
        ],
        new_nodes
        )

    def test_split_no_image(self):
        node = TextNode(
        "This is text with an and another ",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an and another ", TextType.TEXT),
        ],
        new_nodes
        )

    def test_split_image_for_link(self):
        node = TextNode(
        "This is text with a link ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node],new_nodes)