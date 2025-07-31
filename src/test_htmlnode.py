import unittest
from htmlnode import HTMLNode

class HTMLNodeTest(unittest.TestCase):
    def test_ctor(self):
        a = HTMLNode("a", 1234, props={"href": "https://boot.dev"})
        node = HTMLNode("div", children=[a], props={"class": "centered"})

        self.assertEqual(a.tag, "a")
        self.assertEqual(a.value, 1234)
        self.assertEqual(a.children, None)
        self.assertEqual(a.props["href"], "https://boot.dev")
        self.assertEqual(node.value, None)
        self.assertIn(a, node.children)

    def test_props_to_html(self):
        node = HTMLNode(props={
            "class": "centered",
            "width": 800
        })
        props = node.props_to_html()
        self.assertEqual(props, ' class="centered" width="800"')

