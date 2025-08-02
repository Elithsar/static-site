import unittest
from blocknode import BlockType, BlockNode

class TestParser(unittest.TestCase):
    def test_block_to_block_type(self):
        block = BlockNode("# This is a heading")
        self.assertEqual(block.block_type, BlockType.HEADING)
        
        block = BlockNode("This is a paragraph")
        self.assertEqual(block.block_type, BlockType.PARAGRAPH)

        block = BlockNode("```python\nprint('Hello, world!')\n```")
        self.assertEqual(block.block_type, BlockType.CODE)

        block = BlockNode("> This is a quote")
        self.assertEqual(block.block_type, BlockType.QUOTE)
        
        block = BlockNode("- This is an unordered list item")
        self.assertEqual(block.block_type, BlockType.UNORDERED_LIST)
        
        block = BlockNode("1. This is an ordered list item")
        self.assertEqual(block.block_type, BlockType.ORDERED_LIST)
        


