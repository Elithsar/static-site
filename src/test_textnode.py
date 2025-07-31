import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ctor(self):
        node = TextNode("Text", TextType.ITALIC)
        self.assertEqual(node.text, "Text")
        self.assertEqual(node.text_type, TextType.ITALIC)
        self.assertEqual(node.url, None)

    def test_text_node_to_html_node(self):
        text_node = TextNode("Hello, world!", TextType.PLAIN)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello, world!")

        text_node = TextNode("Hello, world!", TextType.BOLD)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "strong")
        self.assertEqual(html_node.value, "Hello, world!")

        text_node = TextNode("Hello, world!", TextType.ITALIC)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "em")
        self.assertEqual(html_node.value, "Hello, world!")

        text_node = TextNode("Hello, world!", TextType.CODE)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello, world!")

        text_node = TextNode("Boot.dev", TextType.LINK, url="https://boot.dev")
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props["href"], "https://boot.dev")

        text_node = TextNode("Image", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "Image")

    def test_text_node_to_html_node_invalid_type(self):
        text_node = TextNode("Invalid", "unknown_type")
        with self.assertRaises(ValueError) as cm:
            text_node.text_node_to_html_node()
        self.assertEqual(str(cm.exception), "Unknown text type: unknown_type")


if __name__ == "__main__":
    unittest.main()
