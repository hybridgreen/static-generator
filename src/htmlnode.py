
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

