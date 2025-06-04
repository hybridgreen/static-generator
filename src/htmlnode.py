
class HTMLNode():
    def __init__(self, tag = None, value=None, children =None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
        pass

    def props_to_html(self):
        text = ""
        if self.props == None:
            return ""
        for key in self.props:
            text += f" {key}=\"{self.props[key]}\""
        return text
    
    def __repr__(self):
        return f" HTML Tag: {self.tag} \n Value:{self.value} \n Children: {self.children} \n Props: {str(self.props)}"
    

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
            parent_html = f"<{self.tag} {self.props_to_html()}>{children_html}</{self.tag}>"
            return parent_html


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
        
