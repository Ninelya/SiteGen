from htmlnodes.htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, 
                 tag: str, 
                 children: list[HTMLNode]):
        super().__init__(tag, None, children, None)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is missing")
        if self.children is None:
            raise ValueError("children are missing")
        result = ""
        for ch in self.children:
            result += ch.to_html()
        return f"<{self.tag}>{result}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children})"

    