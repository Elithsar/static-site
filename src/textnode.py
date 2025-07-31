from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def __iter__(self):
        yield self

    def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.PLAIN:
            return LeafNode(value=text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode(tag="strong", value=text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode(tag="em", value=text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        elif text_node.text_type == TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text})
        else:
            raise ValueError(f"Unknown text type: {text_node.text_type}")
    
