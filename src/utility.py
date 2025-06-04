from textnode import *
from leafnode import *
import re

# ----------------------Nodes Utility ----------------------
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
            if text_node.text == "":
                raise ValueError("Text nodes must have alt text for accesibility")
            return LeafNode("img","",{"src":text_node.url, "alt":text_node.text})
        
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        
        case _:
            raise Exception("Invalid text node type") 
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if not isinstance(text_type, TextType) or delimiter == "":
        raise Exception("Invalid text type or delimiter")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)

            if len(split_node)%2 == 0:
                raise Exception("Invalid delimiter number, please check your syntax")
            
            for index, sub_node in enumerate(split_node):
                if index % 2 == 0:
                    new_nodes.append(TextNode(sub_node, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(sub_node, text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):

    new_nodes = []
    for node in old_nodes:
        if extract_markdown_images(node.text) == []:
            new_nodes.append(node)
        else:
            split_node = re.split(r"(!\[.*?\]\(.*?\))", node.text)
            for index, sub_node in enumerate(split_node):
                if index % 2== 0 and sub_node != "":
                    new_nodes.append(TextNode(sub_node, TextType.TEXT))
                elif sub_node != "":
                    img_md = extract_markdown_images(sub_node)
                    new_nodes.append(TextNode(img_md[0][0], TextType.IMG, img_md[0][1]))
    return new_nodes

    

def split_nodes_link(old_nodes):

    new_nodes = []
    for node in old_nodes:
        if extract_markdown_links(node.text) == []:
            new_nodes.append(node)
        else:
            split_node = re.split(r"(\[.*?\]\(.*?\))", node.text)
            for index, sub_node in enumerate(split_node):
                if index % 2== 0 and sub_node != "":
                    new_nodes.append(TextNode(sub_node, TextType.TEXT))
                elif sub_node != "":
                    link_md = extract_markdown_links(sub_node)
                    new_nodes.append(TextNode(link_md[0][0], TextType.LINK, link_md[0][1]))
    return new_nodes

        