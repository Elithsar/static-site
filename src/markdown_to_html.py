from blocknode import BlockNode
from parentnode import ParentNode

    
def markdown_to_blocks(markdown):
    if not markdown:
        return []

    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def markdown_to_html_node(markdown):
    """Convert a full markdown document into a single HTML node."""
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_node = BlockNode(block)
        children.append(block_node.to_html_node())

    result_node = ParentNode("div", children=children)
    # print(repr(result_node))
    return result_node