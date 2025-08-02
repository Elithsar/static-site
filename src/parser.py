from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown syntax")
        
        i = 0
        
        for part in parts:
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(part, text_type))
            i += 1
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r'!\[([^\]]+)\]\(([^)]+)\)', text)
    images = []
    for match in matches:
        images.append((match[0], match[1]))
    return images

def extract_markdown_links(text):
    matches = re.findall(r'[^!]\[([^\]]+)\]\(([^)]+)\)', text)
    links = []
    for match in matches:
        links.append((match[0], match[1]))
    return links
        