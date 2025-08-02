from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode
from parser import text_to_textnodes
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class BlockNode:
    def __init__(self, text):
        self.text = text
        self.block_type = self.block_to_block_type()

    def __eq__(self, other):
        return (
            self.block == other.block
            and self.block_type == other.block_type
        )

    def __repr__(self):
        return f"BlockNode({self.text}, {self.block_type.value})"

    def __iter__(self):
        yield self

    def block_to_block_type(self):
        is_unordered_list = True
        is_ordered_list = True

        lines = self.text.split("\n")
        for line in lines:
            if not line.startswith("- "):
                is_unordered_list = False
            if not (line[0].isdigit() and line[1] == "."):
                is_ordered_list = False

        if self.text.startswith("# ") or self.text.startswith("## ") or self.text.startswith("### ") or self.text.startswith("#### ") or self.text.startswith("##### ") or self.text.startswith("###### "):
            return BlockType.HEADING
        elif self.text.startswith("```") and self.text.endswith("```"):
            return BlockType.CODE
        elif self.text.startswith("> "):
            return BlockType.QUOTE
        elif is_unordered_list:
            return BlockType.UNORDERED_LIST
        elif is_ordered_list:
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH

    def to_html_node(self):
        if self.block_type == BlockType.PARAGRAPH:
            self.text = self.text.replace("\n", " ")  # Replace newlines with spaces for paragraphs

        if self.block_type == BlockType.CODE:
            children = [LeafNode(tag="code", value=self.text[3:-3].lstrip())] # Remove the code wrapper
        else:
            text_nodes = text_to_textnodes(self.text)
            children = [text_node.text_node_to_html_node() for text_node in text_nodes]
        
        # Determine tag based on block type
        match(self.block_type):
            case BlockType.HEADING:
                tag = "h1" if self.text.startswith("# ") else "h2" if self.text.startswith("## ") else "h3" if self.text.startswith("### ") else "h4" if self.text.startswith("#### ") else "h5" if self.text.startswith("##### ") else "h6"
            case BlockType.CODE:
                tag = "pre"
            case BlockType.QUOTE:
                tag = "blockquote"
            case BlockType.UNORDERED_LIST:
                tag = "ul"
            case BlockType.ORDERED_LIST:
                tag = "ol"
            case BlockType.PARAGRAPH:
                tag = "p"
            case _:
                raise ValueError(f"Unknown block type: {self.block_type}")
        html_node = ParentNode(tag=tag, children=children)
        return html_node
    
