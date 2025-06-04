import re, functools, utility
from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType



__BlockTypes__ = ['paragraph', 'heading', 'code', 'quote', 'ul', 'ol']
BlockType= Enum('BlockType',__BlockTypes__)


# ----------------------Blocks Utility ----------------------

@functools.lru_cache
def markdown_to_blocks(markdown):
    blocks =  markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        if block !="":
            cleaned_blocks.append(block.strip())
    return cleaned_blocks

def block_to_block_type(block):
    if re.search(r"^#{1,6}", block, flags= re.MULTILINE)!= None:
        return BlockType.heading
    
    if  re.search(r"```[\s\S]*?```", block, flags= re.MULTILINE) != None:
        return BlockType.code
    
    if re.search(r"^>", block, flags= re.MULTILINE) != None:
        return BlockType.quote
    
    if re.search(r"^(- )", block, flags= re.MULTILINE) != None:
        return BlockType.ul
    
    if re.search(r"^([\d]. )", block, flags= re.MULTILINE) != None:
        return BlockType.ol
    
    return BlockType.paragraph

def text_to_children(text):
    children = []
    base_node = TextNode(text,TextType.TEXT,None)
    sub_nodes = utility.split_nodes_delimiter([base_node],"**",TextType.BOLD)
    sub_nodes = utility.split_nodes_delimiter(sub_nodes,"_",TextType.ITALIC)
    sub_nodes = utility.split_nodes_delimiter(sub_nodes,"`",TextType.CODE)
    sub_nodes = utility.split_nodes_image(sub_nodes)
    sub_nodes = utility.split_nodes_link(sub_nodes)
    
    for node in sub_nodes:
        children.append(utility.text_node_to_html_node(node))
    return children

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    content = []
    for block in md_blocks:
        match block_to_block_type(block):
            case BlockType.paragraph:
                text = block.strip()
                text = text.replace("\n", " ")
                content.append(ParentNode("p", text_to_children(text),None))
            case BlockType.heading:
                h_count = block.strip().count("#")
                text = block.replace("#", "")
                text = text.strip()
                content.append(LeafNode(f"h{h_count}", text, None))
            case BlockType.quote:
                text = block.replace(">", "").strip()
                content.append(ParentNode("blockquote",text_to_children(text),None))
            case BlockType.ul:
                text = block.replace("- ", "<li>")
                text = text.replace("\n", "</li>")
                content.append(ParentNode("ul",text_to_children(text),None))
            case BlockType.ol:
                text = re.sub(r"^([\d]. )", "<li>", block, 0, re.MULTILINE)
                text = text.replace("\n", "</li>")
                content.append(ParentNode("ol",text_to_children(text), None))

            case BlockType.code:
                text =re.sub(r"```", "", block)
                code =LeafNode("code",text.lstrip(), None)
                content.append(ParentNode("pre",[code], None))

    return ParentNode("div",content, {"class":"container"})

