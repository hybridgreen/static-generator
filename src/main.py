from textnode import *
from leafnode import * 
import os , re, blocks, utility
from os import path
from shutil import copy, rmtree

def copy_to_public(source, dest):
    source_cont = os.listdir(source)
    for item in source_cont:
        item_path = path.join(source,item)
        if path.isfile(item_path):
            copy(item_path, dest)
        else:
            d_dir_path = path.join(dest,item)
            os.mkdir(d_dir_path)
            copy_to_public(item_path,d_dir_path)
    pass

def extract_title(markdown):
    if not re.search(r"^(#\s)", markdown):
        raise Exception("Invalid markdown- Page must have a # Title")
    
    md_blocks = blocks.markdown_to_blocks(markdown) #to be deleted
    for block in md_blocks:
        if re.search(r"^(#\s)", block):
            return block[1:].strip()
            
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from:\n -{from_path}\n -to {dest_path}\n -using {template_path}")

    md_file = open(from_path)
    markdown = md_file.read()
    md_file.close()

    tp_file = open(template_path)
    template = tp_file.read()

    

    pass

def main():
    #Set working directory and establish project structure
    project_dir = os.getcwd()
    static_dir = path.join(project_dir,"static")
    public_dir = path.join(project_dir,"public")

    # Create a clean public directory
    rmtree(public_dir)
    os.mkdir(public_dir)

    #Copy static content to public directory
    if path.exists(static_dir):
        copy_to_public(static_dir, public_dir)
    else: 
        print("Path error")
        raise Exception("Path error")
    pass

main()

