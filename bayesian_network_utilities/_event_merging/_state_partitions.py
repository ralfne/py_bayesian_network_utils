class _StatePartitions(object):
    def __init__(self, dist_event_merge_defs, bayesian_network):
        self._bayesian_network = bayesian_network
        root_name = dist_event_merge_defs.get_root_state_name()
        # states changed by merging events:
        self.merged_state_names = self._get_merged_state_names(root_name)
        # states affected by merge; ie. changed states +  states whose ancestors are changed
        self.affected_state_names = self._get_affected_state_names(root_name)
        # states not affected by merge; i.e. all ancestors of the to-be-merged state
        self.unaffected_state_names = self._get_unaffected_state_names()

    def _get_merged_state_names(self, root_name):
        out = self._get_children_names(root_name, include_parent=True)
        return out

    def _get_affected_state_names(self, root_name):
        out = [root_name]
        self._get_offspring_names(root_name, out)
        return out

    def _get_unaffected_state_names(self):
        out = []
        for state in self._bayesian_network.states:
            if state.name not in self.affected_state_names:
                out.append(state.name)
        return out

    def _get_children_names(self, edge_name, include_parent=False):
        out = []
        if include_parent: out.append(edge_name)
        for e in self._bayesian_network.edges:
            e0 = e[0]
            e1 = e[1]
            if e0.name==edge_name: out.append(e1.name)
        return out

    def _get_offspring_names(self, state_name, offspring_names):
        for e in self._bayesian_network.edges:
            e0 = e[0]
            e1 = e[1]
            if e0.name == state_name:
                offspring_names.append(e1.name)
                self._get_offspring_names(e1.name, offspring_names)
