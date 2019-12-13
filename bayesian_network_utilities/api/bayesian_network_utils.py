import pomegranate as pg
from pomegranate.distributions import DiscreteDistribution, ConditionalProbabilityTable


class BayesianNetworkUtils(object):

    @staticmethod
    def get_edge(bayesian_network, statename_from, statename_to):
        for e1, e2 in bayesian_network.edges:
            if (e1.name == statename_from) and (e2.name == statename_to):
                return e1, e2
        return None

    @staticmethod
    def get_states(bayesian_network):
        out = []
        if isinstance(bayesian_network, pg.BayesianNetwork):
            for s in bayesian_network.states:
                out.append(s)
        else: raise NotImplementedError()
        return out

    @staticmethod
    def get_statenames(bayesian_network):
        out = []
        if isinstance(bayesian_network, pg.BayesianNetwork):
            for s in bayesian_network.states:
                out.append(s.name)
        else: raise NotImplementedError()
        return out

    @staticmethod
    def assert_states_structures_equality(state1, state2):
        if (isinstance(state1.distribution, DiscreteDistribution)) and \
            (isinstance(state2.distribution, DiscreteDistribution)):
            BayesianNetworkUtils._assert_discrete_distribution_structures_equality(state1, state2)
        elif (isinstance(state1.distribution, ConditionalProbabilityTable)) and \
            (isinstance(state2.distribution, ConditionalProbabilityTable)):
            BayesianNetworkUtils._assert_conditional_probability_table_structures_equality(state1, state2)
        else: raise AssertionError("Incompatible distribution types for '%s' and '%s"
                                   % (state1.name, state2.name))

    @staticmethod
    def _assert_discrete_distribution_structures_equality(state1, state2):
        params1 = state1.distribution.parameters[0]
        params2 = state2.distribution.parameters[0]
        if len(params1) != len(params2): raise AssertionError('Number of probabilities not equal')
        for key in params1.keys():
            if not params2.has_key(key): raise AssertionError("Probability '%s' not found" % key)

    @staticmethod
    def _assert_conditional_probability_table_structures_equality(state1, state2):
        params1 = state1.distribution.parameters[0]
        params2 = state2.distribution.parameters[0]
        if len(params1) != len(params2): raise AssertionError("Number of probabilities for '%s' and '%s' not equal"
                                                              % (state1.name, state2.name) )
        for item1, item2 in zip(params1, params2):
            if len(item1) != len(item2): raise AssertionError("Number of conditions for '%s' and '%s' not equal"
                                                              % (state1.name, state2.name))
            for i in range(len(item1)-1):
                v1 = item1[i]
                v2 = item2[i]
                if v1 != v2: raise AssertionError("Conditions for '%s' and '%s' not equal"
                                                  % (state1.name, state2.name))

    @staticmethod
    def get_state(bayesian_network, name):
        if isinstance(bayesian_network, pg.BayesianNetwork):
            for s in bayesian_network.states:
                if s.name == name: return s
        else: raise NotImplementedError()
        return None

    @staticmethod
    def all_event_names_are_unique(bayesian_network):
        if isinstance(bayesian_network, pg.BayesianNetwork):
            events = {}
            for s in bayesian_network.states:
                dist = s.distribution
                if isinstance(dist, DiscreteDistribution):
                    for key, value in dist.parameters[0].iteritems():
                        if events.has_key(key): return False
                        events[key] = key
                elif isinstance(dist, ConditionalProbabilityTable):
                    outcomes = {}
                    for item in dist.parameters[0]:
                        key = item[-2]
                        outcomes[key] = key
                    for key, item in outcomes.iteritems():
                        if events.has_key(key): return False
                        events[key] = key
            return True
        else: raise NotImplementedError()