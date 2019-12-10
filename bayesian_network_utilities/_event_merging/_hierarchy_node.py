class _HierarchyNode(object):
    def __init__(self, name):
        self.name = name
        self.parents = {}
        self.children = {}