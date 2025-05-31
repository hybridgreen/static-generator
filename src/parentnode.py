from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("Parent node must have a tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Parent node must have children")
        else:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
            parent_html = f"<{self.tag}>{children_html}</{self.tag}>"
            return parent_html
             