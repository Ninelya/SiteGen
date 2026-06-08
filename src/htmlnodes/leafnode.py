from htmlnodes.htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, 
                 tag: str|None, 
                 value: str, 
                 props: dict[str, str]|None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is missing")
        return self.render()
        
    def __repr__(self):
        return f"HTMLNode:\ntag = {self.tag}\nvalue = {self.value}\nprops = {self.props}"
    
    def render(self):
       match self.tag:
            case None:
               return self.value
            case "p" | "b" | "i" | "code" | "span" | "div":
               return f"<{self.tag}>{self.value}</{self.tag}>"
            case "a":
               return f"<a{self.props_to_html()}>{self.value}</a>"
            case "img":
               return f"<img{self.props_to_html()} />"