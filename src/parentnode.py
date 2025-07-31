from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        children_html = ""

        for child in self.children:
            children_html += child.to_html()
            
        props_html = self.props_to_html() if self.props else ""

        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f'ParentNode(tag="{self.tag}", children={repr(self.children)}, props={repr(self.props)})'


