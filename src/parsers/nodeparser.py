import re
from nodes.textnode import *
from htmlnodes.leafnode import *

def text_to_htmlnodes(text: str) -> list[LeafNode]:
    if text == "":
        return []
    nodes = text_to_textnodes(text)
    return [node.text_node_to_leaf_node() for node in nodes]

def text_to_textnodes(text: str) -> list[TextNode]:
    if text == "":
        return []
    nodes = split_nodes_delimiter([TextNode(text, TextType.PLAIN)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

def split_nodes_delimiter(
        old_nodes: list[TextNode], 
        delimiter: str,
        text_type: TextType
        ) -> list[TextNode]:
    
    result = []
    for node in old_nodes:
        # some other node:
        if node.text_type != TextType.PLAIN:
            result.append(node)
            continue

        nodes_count = node.text.count(delimiter)
        if  nodes_count % 2 != 0:
            raise Exception("invalid Markdown syntax")
        
        new_nodes = []    

        # other nodes, if present:
        splitted = node.text.split(delimiter)
        current_type = TextType.PLAIN
        for i in range(len(splitted)):
            if splitted[i] != "":
                new_nodes.append(TextNode(splitted[i], current_type))
            current_type = TextType.PLAIN if current_type == text_type else text_type
        result.extend(new_nodes)
    return result

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_images_links(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_images_links(old_nodes, TextType.LINK)    

def split_nodes_images_links(old_nodes: list[TextNode], type: TextType) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result.append(node)
            continue

        props = extract_markdown_images(node.text) if type == TextType.IMAGE else extract_markdown_links(node.text)
        if len(props) == 0:
            result.append(node)
            continue

        current_text = node.text
        for prop in props:
            prefix = "!" if type == TextType.IMAGE else ""
            pattern = f"{prefix}[{prop[0]}]({prop[1]})"
            sections = current_text.split(pattern, 1)
            if len(sections) != 2:
                raise ValueError(f"invalid markdown, {type.value} section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.PLAIN))
            result.append(TextNode(prop[0], type, prop[1]))
            current_text = sections[1]
        if current_text != "":
            result.append(TextNode(current_text, TextType.PLAIN))
    return result
