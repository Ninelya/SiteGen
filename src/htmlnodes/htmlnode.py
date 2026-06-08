

class HTMLNode:
    def __init__(self, 
                 tag: str|None = None, 
                 value: str|None = None, 
                 children: list[HTMLNode]|None = None,  
                 props: dict[str, str]|None = None):
        self.tag: str|None = tag
        self.value: str|None = value
        self.children: list[HTMLNode]|None = children
        self.props: dict[str, str]|None = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        result = ""
        if self.props:
            for key, value in self.props.items():
                result += f" {key}=\"{value}\""
        return result

    def __repr__(self):
        return f"HTMLNode:\ntag = {self.tag}\nvalue = {self.value}\nchildren = {self.children}\nprops = {self.props}"