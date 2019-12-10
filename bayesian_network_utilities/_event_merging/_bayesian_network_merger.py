from pomegranate import *

from bayesian_network_utilities._event_merging._conditional_items import _ConditionalItems
from bayesian_network_utilities._event_merging._conditional_items_merger import _ConditionalItemsMerger
from _hierarchy_node import _HierarchyNode
from bayesian_network_utilities._event_merging._state_partitions import _StatePartitions
from bayesian_network_utilities.api.bayesian_network_utils import BayesianNetworkUtils


class _BayesianNetworkMerger:
    def __init__(self, distribution_merge_definitions):
        self._distribution_merge_defs = distribution_merge_definitions
        self._bayesian_network = self._distribution_merge_defs.get_bayesian_network()
        self._hierarchy_nodes = self._create_hierarchy_nodes()
        self._state_partitions = _StatePartitions(self._distribution_merge_defs, self._bayesian_network)

    def _create_hierarchy_nodes(self):
        out = {}
        for parent, child in self._bayesian_network.edges:
            p_node = out.get(parent.name)
            if p_node is None:
                p_node = _HierarchyNode(parent.name)
                out[p_node.name] = p_node
            c_node = out.get(child.name)
            if c_node is None:
                c_node = _HierarchyNode(child.name)
                out[c_node.name] = c_node
            p_node.children[c_node.name] = c_node
            c_node.parents[p_node.name] = p_node
        return out

    def _get_hierarchy_path(self, root_node, path):
        path.append(root_node.name)
        for key, value in root_node.children.iteritems():
            self._get_hierarchy_path(value, path)
        return path

    # def _get_state(self, name):
    #     out = BayesianNetworkWrapper.get_state(self._bayesian_network, name)
    #     return out

    def create_merged_bayesian_network(self):
        merged_nodes = {}
        for state_name in self._state_partitions.merged_state_names:
            state = BayesianNetworkUtils.get_state(self._bayesian_network, state_name)
            tmp = _ConditionalItems(state.distribution)
            merged_node = _ConditionalItems()
            for merge_def in self._distribution_merge_defs:
                splits = _ConditionalItemsMerger(tmp, merge_def)
                merged_items = splits.create_merged_items(merge_def)
                merged_node.extend(merged_items)
            if not self._distribution_merge_defs.get_allow_unspecified_events():
                merged_node = self._cull_merged_node(merged_node)
            merged_nodes[state_name] = merged_node
        out = self._create_bayesian_network(merged_nodes)
        return out

    def _cull_merged_node(self, merged_node):
        out = _ConditionalItems()
        for item in merged_node:
            for key in self._distribution_merge_defs.get_merged_eventnames():
                if item.has_condition_or_outcome(key):
                    out.add_item(item)
        return out

    def _create_bayesian_network(self, merged_nodes):
        out = BayesianNetwork(self._bayesian_network.name)
        self._add_unaffected_states(out)
        self._add_affected_states(merged_nodes, out)
        self._add_edges(out)
        return out

    def _add_unaffected_states(self, bayesian_network):
        for state_name in self._state_partitions.unaffected_state_names:
            state = BayesianNetworkUtils.get_state(self._bayesian_network, state_name)
            bayesian_network.add_state(state)

    def _add_edges(self, bayesian_network):
        for e0, e1 in self._bayesian_network.edges:
            new_e0 = BayesianNetworkUtils.get_state(bayesian_network, e0.name)
            new_e1 = BayesianNetworkUtils.get_state(bayesian_network, e1.name)
            bayesian_network.add_edge(new_e0, new_e1)

    def _add_affected_states(self, merged_nodes, bayesian_network):
        affected_states = {}
        for name in self._state_partitions.affected_state_names:
            affected_states[name] = name
        while (len(affected_states) > 0):
            added_keys = []
            for key, affected_state_name in affected_states.iteritems():
                added = self._try_add_affected_state(affected_state_name, merged_nodes, bayesian_network)
                if added: added_keys.append(key)
            for key in added_keys:
                del affected_states[key]

    def _try_add_affected_state(self, affected_state_name, merged_nodes, bayesian_network):
        merged_node = merged_nodes.get(affected_state_name)
        if merged_node is None:
            # only the parent nodes are directly affected, not the node itself
            return self._try_add_indirectly_affected_state(affected_state_name, bayesian_network)
        else:
            # the node itself is affected
            return self._try_add_directly_affected_state(merged_node, affected_state_name, bayesian_network)

    def _try_add_directly_affected_state(self, merged_node, original_state_name, bayesian_network):
        original_state_node = self._hierarchy_nodes.get(original_state_name)
        parents = []
        for p in original_state_node.parents:
            new_parent = BayesianNetworkUtils.get_state(bayesian_network, p)
            if new_parent is None: return False
            parents.append(new_parent.distribution)
        if len(parents) == 0: parents = None
        probs = merged_node.export_probabilities(parents)
        state = Node(probs, name=original_state_name)
        bayesian_network.add_state(state)
        return True

    def _try_add_indirectly_affected_state(self, original_state_name, bayesian_network):
        hierarchy_node = self._hierarchy_nodes.get(original_state_name)
        parents = []
        for p in hierarchy_node.parents:
            new_parent = BayesianNetworkUtils.get_state(bayesian_network, p)
            if new_parent is None: return False
            new_parent = new_parent.distribution
            parents.append(new_parent)
        original_state = BayesianNetworkUtils.get_state(self._bayesian_network, original_state_name)
        probs = original_state.distribution.parameters[0]
        cpt =  ConditionalProbabilityTable(probs, parents)
        state = Node(cpt, name=original_state_name)
        bayesian_network.add_state(state)
        return True

