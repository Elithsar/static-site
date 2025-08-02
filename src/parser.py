from textnode import TextNode, TextType
from htmlnode import HTMLNode
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

def split_nodes_image(old_nodes):
    old_nodes_copy = old_nodes.copy()
    new_nodes = []

    for node in old_nodes_copy:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
                
        for match in matches:
            search_text = f"![{match[0]}]({match[1]})"
            index = node.text.index(search_text)
            new_nodes.append(TextNode(node.text[:index], TextType.PLAIN))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            node.text = node.text[index + len(search_text):]
        # Add any remaining text after the last match
        if node.text:
            new_nodes.append(TextNode(node.text, TextType.PLAIN))
            
    return new_nodes

def split_nodes_link(old_nodes):
    old_nodes_copy = old_nodes.copy()
    new_nodes = []

    for node in old_nodes_copy:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
                
        for match in matches:
            search_text = f"[{match[0]}]({match[1]})"
            index = node.text.index(search_text)
            new_nodes.append(TextNode(node.text[:index], TextType.PLAIN))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            node.text = node.text[index + len(search_text):]
        # Add any remaining text after the last match
        if node.text:
            new_nodes.append(TextNode(node.text, TextType.PLAIN))
            
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

def text_to_textnodes(text):
    if not text:
        return []    
    initial_text_node = TextNode(text, TextType.PLAIN)
    nodes = split_nodes_delimiter(initial_text_node, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes




        