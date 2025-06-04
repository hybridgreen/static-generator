from htmlnode import *


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag,value,None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All nodes must have a value")
        if self.tag == None:
            return self.value
        if self.tag == "img":
                return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        