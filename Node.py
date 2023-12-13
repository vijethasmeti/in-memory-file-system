class Node:
    def __init__(self, name, is_dir=False,children={},content="" ,parent=None):
        self.name = name
        self.is_dir = is_dir
        self.children = {}
        self.content = content
        self.parent = parent