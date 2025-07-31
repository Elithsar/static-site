class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return None

        text = " "

        for k, v in self.props.items():
            text += f'{k}="{v}" '

        return text[:-1]

    def __repr__(self):
        return f'HTMLNode(tag="{self.tag}", value="{self.value}", children={repr(self.children)}, props={repr(self.props)}"'

    def __iter__(self):
        for node in self.children:
            yield node
