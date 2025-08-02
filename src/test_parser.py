import unittest
from htmlnode import HTMLNode
from textnode import TextNode, TextType
from parser import *
from markdown_to_html import markdown_to_html_node, markdown_to_blocks

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

    # markdown images tests
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_images(
            "This is text with no image an ![image]()"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_images(
            "This is text with no image an ![](efzfzef)"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_images(
            "This is text with no image [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    # markdown link tests
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

        matches = extract_markdown_links(
            "This is text with no link an [link]()"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_links(
            "This is text with no link an [](link.com)"
        )
        self.assertListEqual([], matches)

    # node parsing images tests
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image_001](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image_001", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # node parsing links tests
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.google.com")
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.bing.com)!",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://www.bing.com"),
                TextNode("!", TextType.PLAIN),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is a **bold** and _italic_ and `code` text with a [link](https://www.google.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        nodes = text_to_textnodes(text)
        
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            nodes,
        )
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        md = """


This is another **bolded** para**gra**ph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
- and more items



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is another **bolded** para**gra**ph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items\n- and more items",
            ],
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

