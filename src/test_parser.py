import unittest
from htmlnode import HTMLNode
from textnode import TextNode, TextType
from parser import split_nodes_delimiter

class TestParser(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        text = TextNode("this is `code` for real", TextType.PLAIN)
        nodes = split_nodes_delimiter(text, "`", TextType.CODE)

        self.assertEqual(3, len(nodes))
        self.assertEqual("this is ", nodes[0].text)
        self.assertEqual(TextType.PLAIN, nodes[0].text_type)
        self.assertEqual(None, nodes[0].url)
        self.assertEqual("code", nodes[1].text)
        self.assertEqual(TextType.CODE, nodes[1].text_type)
        self.assertEqual(None, nodes[1].url)
        self.assertEqual(" for real", nodes[2].text)
        self.assertEqual(TextType.PLAIN, nodes[2].text_type)
        self.assertEqual(None, nodes[2].url)

    def test_split_nodes_delimiter_bold(self):
        text = TextNode("this is **bold** for real", TextType.PLAIN)
        nodes = split_nodes_delimiter(text, "**", TextType.BOLD)

        self.assertEqual(3, len(nodes))
        self.assertEqual("this is ", nodes[0].text)
        self.assertEqual(TextType.PLAIN, nodes[0].text_type)
        self.assertEqual(None, nodes[0].url)
        self.assertEqual("bold", nodes[1].text)
        self.assertEqual(TextType.BOLD, nodes[1].text_type)
        self.assertEqual(None, nodes[1].url)
        self.assertEqual(" for real", nodes[2].text)
        self.assertEqual(TextType.PLAIN, nodes[2].text_type)
        self.assertEqual(None, nodes[2].url)

    def test_split_nodes_delimiter_italic(self):
        text = TextNode("this is _italic_ for real", TextType.PLAIN)
        nodes = split_nodes_delimiter(text, "_", TextType.ITALIC)

        self.assertEqual(3, len(nodes))
        self.assertEqual("this is ", nodes[0].text)
        self.assertEqual(TextType.PLAIN, nodes[0].text_type)
        self.assertEqual(None, nodes[0].url)
        self.assertEqual("italic", nodes[1].text)
        self.assertEqual(TextType.ITALIC, nodes[1].text_type)
        self.assertEqual(None, nodes[1].url)
        self.assertEqual(" for real", nodes[2].text)
        self.assertEqual(TextType.PLAIN, nodes[2].text_type)
        self.assertEqual(None, nodes[2].url)

    def test_split_nodes_delimiter_multiple(self):
        text = TextNode("this is `code` and **bold** and _italic_ for real", TextType.PLAIN)
        nodes = split_nodes_delimiter(text, "`", TextType.CODE)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(7, len(nodes))
        self.assertEqual("this is ", nodes[0].text)
        self.assertEqual(TextType.PLAIN, nodes[0].text_type)
        self.assertEqual(None, nodes[0].url)    
        self.assertEqual("code", nodes[1].text)
        self.assertEqual(TextType.CODE, nodes[1].text_type)
        self.assertEqual(None, nodes[1].url)
        self.assertEqual(" and ", nodes[2].text)
        self.assertEqual(TextType.PLAIN, nodes[2].text_type)
        self.assertEqual(None, nodes[2].url)
        self.assertEqual("bold", nodes[3].text)
        self.assertEqual(TextType.BOLD, nodes[3].text_type)
        self.assertEqual(None, nodes[3].url)
        self.assertEqual(" and ", nodes[4].text)
        self.assertEqual(TextType.PLAIN, nodes[4].text_type)        
        self.assertEqual(None, nodes[4].url)
        self.assertEqual("italic", nodes[5].text)
        self.assertEqual(TextType.ITALIC, nodes[5].text_type)       
        self.assertEqual(None, nodes[5].url)
        self.assertEqual(" for real", nodes[6].text)    
        self.assertEqual(TextType.PLAIN, nodes[6].text_type)
        self.assertEqual(None, nodes[6].url)  

    def test_split_nodes_delimiter_invalid_syntax(self):
        text = TextNode("this is `code for real", TextType.PLAIN)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter(text, "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "Invalid markdown syntax")

