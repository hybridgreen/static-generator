from textnode import *
from leafnode import *

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text,None)
        
        case TextType.BOLD:
            return LeafNode("b",text_node.text,None)
        
        case TextType.ITALIC:
            return LeafNode("i",text_node.text,None)
        
        case TextType.CODE:
            return LeafNode("code",text_node.text,None)
        
        case TextType.IMG:
            return LeafNode("img","",{"src":text_node.url, "alt":text_node.text})
        
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        
        case _:
            raise Exception("Invalid text node type") 