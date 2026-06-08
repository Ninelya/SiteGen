from nodes.blocknode import *

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)

    root = ParentNode("div", [])
    for block in blocks:
        block_node = block_to_block_node(block)
        parent = block_node.block_node_to_parent_node()
        root.children.append(parent)
    
    return root

def block_to_block_node(block: str) -> BlockNode:
        type = block_to_block_type(block)
        children = None
        text = ""
        lines = block.split("\n")
        heading_number = None
        match type:
            case BlockType.OLIST:
                new_lines = remove_ordered_list_prefix(lines)
                children = [BlockNode(line, BlockType.LITEM) for line in new_lines]
            case BlockType.ULIST:
                children = [BlockNode(line.lstrip("- "), BlockType.LITEM) for line in lines]
            case BlockType.PARAGRAPH:
                text =  " ".join(line.lstrip() for line in lines)
            case BlockType.CODE:
                text = block.strip("```").lstrip("\n")
            case BlockType.HEADING:
                heading_number = len(block)-len(block.lstrip('#'))
                text = block.lstrip("#").lstrip()
            case BlockType.QUOTE:
                text =  " ".join(line.lstrip(">").lstrip() for line in lines)

        return BlockNode(text, type, children, heading_number)

def remove_ordered_list_prefix(lines: list[str]) -> list[str]:
    result = []
    i = 1
    for line in lines:
        result.append(line.lstrip(f"{i}. "))
        i += 1

    return result

def markdown_to_blocks(markdown: str) -> list[str]:
    if markdown == "":
        return []
    lines = markdown.split("\n\n")
    result = []
    for line in lines:
        if line.strip() != "":
            result.append(line.strip())
    return result

def extract_title(markdown: str) -> str|None:
    blocks = markdown_to_blocks(markdown)
    block_nodes = [block_to_block_node(block) for block in blocks]
    for node in block_nodes:
        if (node.block_type == BlockType.HEADING 
            and node.heading_number == 1):
            return node.text
    raise Exception("title not found")