from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        props_html = self.props_to_html() if self.props else ""
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f'LeafNode(tag="{self.tag}", value="{self.value}", props={repr(self.props)})'


