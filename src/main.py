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

    with open(from_path) as md_file:
        markdown = md_file.read()
        print ("Markdown file read: Success!")
    md_file.close()

    with open(template_path) as tp_file:
        template = tp_file.read()
        print ("Template file read: Success!")
    tp_file.close()

    print("Extracting Markdown from file")
    try:
        title = extract_title(markdown)
        content = blocks.markdown_to_html_node(markdown).to_html()
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", content)
        print ("Markdown extraction: Success!")
    except Exception as e:
        print("Markdown extraction: Failed")
        print(e)

    if not path.exists(dest_path):
        os.mkdir(dest_path)
    index_path = path.join(dest_path, "index.html")
    index = open(index_path, 'w')
    index.write(template)
    index.close()

    pass

def main():
    #Set working directory and establish project structure
    project_dir = os.getcwd()
    static_dir = path.join(project_dir,"static")
    public_dir = path.join(project_dir,"public")
    index_md = path.join(project_dir,"content/index.md")
    template_path = path.join(project_dir,"template.html")

    # Create a clean public directory
    rmtree(public_dir)
    os.mkdir(public_dir)

    #Copy static content to public directory
    if path.exists(static_dir):
        copy_to_public(static_dir, public_dir)
    else: 
        print("Path error")
        raise Exception("Path error")
    

    generate_page(index_md, template_path,public_dir)
    pass

main()

