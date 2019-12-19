from enum import Enum
import pandas as pd
from pomegranate.distributions.ConditionalProbabilityTable import ConditionalProbabilityTable
from pomegranate.distributions.DiscreteDistribution import DiscreteDistribution

from bayesian_network_utilities._event_merging.bayesian_network_merger import BayesianNetworkMerger
from bayesian_network_utilities._event_merging.marginals_parser import MarginalsParser
import pomegranate as pg

from bayesian_network_utilities.api.bayesian_network_utils import BayesianNetworkUtils


class ProbabilityType(Enum):
    Marginal = 0
    Conditional =1


class BayesianNetworkWrapper(object):
    def __init__(self, pomegranate_bayesian_network, enable_caching=True):
        if not isinstance(pomegranate_bayesian_network, pg.BayesianNetwork):
            raise NotImplementedError()
        self._network = pomegranate_bayesian_network
        self._marginals_parser = MarginalsParser(self._network)
        self._cache = None
        if enable_caching:
            self._cache = {}

    def get_network(self):
        return self._network

    def get_state(self, statename):
        out = BayesianNetworkUtils.get_state(self._network, statename)
        return out

    def get_states(self):
        out = BayesianNetworkUtils.get_states(self._network)
        return out

    def get_edge(self, statename_from, statename_to):
        out = BayesianNetworkUtils.get_edge(self._network, statename_from, statename_to)
        return out

    def get_probabilities(self, statename=None, probability_type=ProbabilityType.Marginal):
        if self._cache is None:
            out = self._create_probabilities(statename, probability_type)
        else:
            key = self._get_probability_key(statename, probability_type)
            out = self._cache.get(key, None)
            if out is None:
                out = self._create_probabilities(statename, probability_type)
                self._cache[key] = out
        return out

    def _get_probability_key(self, statename=None, probability_type=ProbabilityType.Marginal):
        return str(statename) + '_' + str(probability_type)

    def _create_probabilities(self, statename=None, probability_type=ProbabilityType.Marginal):
        out = {}
        if statename is None:
            states = BayesianNetworkUtils.get_statenames(self._network)
            for s in states:
                probs = self._get_probabilities_from_statename(s, probability_type)
                out[s] = probs
        else:
            series = self._get_probabilities_from_statename(statename, probability_type)
            out = series
        return out

    def _get_probabilities_from_statename(self, statename, probability_type=ProbabilityType.Marginal):
        if probability_type == ProbabilityType.Marginal:
            p = self._marginals_parser.get_marginals(statename)
            out = pd.Series(p)
        elif probability_type == ProbabilityType.Conditional:
            state = BayesianNetworkUtils.get_state(self._network, statename)
            dist_params = state.distribution.parameters[0]
            if isinstance(state.distribution, DiscreteDistribution):
                data = []
                for key, value in dist_params.iteritems():
                    row = [value, key, '']
                    data.append(row)
                out = pd.DataFrame(data=data, columns=['p', 'outcome', 'conditions'])
            elif isinstance(state.distribution, ConditionalProbabilityTable):
                data = []
                for item in dist_params:
                    row = [item[-1], item[-2]]
                    conditions = ''
                    for i in range(len(item)-2):
                        if len(conditions) != 0: conditions += ', '
                        conditions += item[i]
                    row.append(conditions)
                    data.append(row)
                out = pd.DataFrame(data=data, columns=['p', 'outcome', 'conditions'])
            else: raise NotImplementedError()
        else: raise NotImplementedError()
        return out

    def create_network_with_merged_events(self, distribution_merge_defs, bake=True):
        merger = BayesianNetworkMerger(distribution_merge_defs)
        out = merger.create_merged_bayesian_network()
        if bake: out.bake()
        return out

    def assert_structure_equality(self, bayesian_network_wrapper):
        self._assert_states_equality(bayesian_network_wrapper)
        self._assert_edges_equality(bayesian_network_wrapper)

    def _assert_states_equality(self, bayesian_network_wrapper):
        if len(self.get_states()) != len(bayesian_network_wrapper.get_states()):
            raise AssertionError('Number of states not equal')
        for state in self.get_states():
            other_state = bayesian_network_wrapper.get_state(state.name)
            if other_state is None: raise AssertionError("State '%s' not found" % state.name)
            BayesianNetworkUtils.assert_states_structures_equality(state, other_state)

    def _assert_edges_equality(self, bayesian_network_wrapper):
        for s1, s2 in self._network.edges:
            other_s1, other_s2 = bayesian_network_wrapper.get_edge(s1.name, s2.name)
            if (other_s1 is None) or (other_s2 is None):
                raise AssertionError("Edge not found for '%s' and '%s'" % (s1.name, s2.name))
