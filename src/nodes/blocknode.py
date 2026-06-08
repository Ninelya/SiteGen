from enum import Enum
from htmlnodes.leafnode import *
from htmlnodes.parentnode import *
from parsers.nodeparser import *

class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    ULIST = "unordered_list",
    OLIST = "ordered_list",
    LITEM = "list_item",

def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif (
        block.startswith("```\n")
        and block.endswith("```")
    ):
        return BlockType.CODE
    else:
        lines: list[str] = block.split("\n")
        if all_lines_start_with_prefix(lines, ">"):
            return BlockType.QUOTE
        elif all_lines_start_with_prefix(lines, "- "):
            return BlockType.ULIST
        elif all_lines_start_with_number(lines):
            return BlockType.OLIST
    return BlockType.PARAGRAPH
    
def all_lines_start_with_prefix(lines: list[str], prefix: str) -> bool:
    for line in lines:
        if not line.startswith(prefix):
            return False
    return True

def all_lines_start_with_number(lines: list[str]) -> bool:
    i = 1
    for line in lines:
        if not line.startswith(f"{i}. "):
            return False
        i += 1
    return True

class BlockNode:
    def __init__(self, 
                 text: str, 
                 type: BlockType, 
                 children: list[BlockNode]|None = None,
                 heading_number: int|None = None) -> None:
        self.text: str = text
        self.block_type: BlockType = type
        self.children: list[BlockNode]|None = children
        self.heading_number = heading_number
           
    def __eq__(self, other: BlockType):
        return (self.text == other.text
                and self.block_type == other.block_type
                and self.tag == other.tag)
                
    def __repr__(self) -> str:
        return f"BlockNode({self.block_type.value}, {self.text}, {self.children})"
    
    def block_node_to_parent_node(self) -> ParentNode:
        match self.block_type:
            case BlockType.PARAGRAPH:
                return ParentNode("p", children = text_to_htmlnodes(self.text))
            case BlockType.HEADING:
                return ParentNode(f"h{self.heading_number}", children = text_to_htmlnodes(self.text))
            case BlockType.CODE:
                return ParentNode("pre", children = [LeafNode("code", self.text)])
            case BlockType.QUOTE:
                return ParentNode("blockquote", children = text_to_htmlnodes(self.text))
            case BlockType.OLIST:
                children = [ParentNode("li", children = text_to_htmlnodes(child.text)) for child in self.children]
                return ParentNode("ol", children = children)
            case BlockType.ULIST:
                children = [ParentNode("li", children = text_to_htmlnodes(child.text)) for child in self.children]
                return ParentNode("ul", children = children)
            case BlockType.LITEM:
                pass
            case _:
                raise Exception("unknown block type")
            