from enum import Enum
from htmlnodes.leafnode import *

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str|None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextType):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)
                
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_leaf_node(self) -> LeafNode:
        match self.text_type:
            case TextType.PLAIN:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                props = {"href": self.url}
                return LeafNode("a", self.text, props)
            case TextType.IMAGE:
                props = {"src": self.url, "alt": self.text}
                return LeafNode("img", "", props)
            case _:
                raise Exception("unknown text type")
