from enum import Enum
import re

__BlockTypes__ = ['paragraph', 'heading', 'code', 'quote', 'ul', 'ol']
BlockType= Enum('BlockType',__BlockTypes__)


# ----------------------Blocks Utility ----------------------

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

