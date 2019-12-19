class _HierarchyNode(object):
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.children = []

    def __str__(self):
        return self.name

class _HierarchyNodes(object):
    def __init__(self, bayesian_network):
        self.nodes = {}
        for index, parents in enumerate(bayesian_network.structure):
            dist = bayesian_network.states[index]
            statename = dist.name
            if len(parents)==0:
                self.nodes[statename] = _HierarchyNode(statename)
            else:
                cnode = self.nodes.get(statename, None)
                if cnode is None:
                    cnode = _HierarchyNode(statename)
                    self.nodes[statename] = cnode
                for p_index in parents:
                    dist = bayesian_network.states[p_index]
                    statename = dist.name
                    p_node = self.nodes.get(statename, None)
                    if p_node is None:
                        p_node = _HierarchyNode(statename)
                        self.nodes[statename] = p_node
                    cnode.parents.append(p_node)
                    p_node.children.append(cnode)
        self.roots = {}
        for key, node in self.nodes.iteritems():
            if len(node.parents) == 0:
                self.roots[key] = node

    def get_node(self, name):
        return self.nodes.get(name, None)

    def get_root_node(self, name):
        return self.roots.get(name, None)