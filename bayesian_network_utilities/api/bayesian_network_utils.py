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
        # params1 = state1
        # params2 = state2
        params1 = state1.distribution.parameters[0]
        params2 = state2.distribution.parameters[0]
        if len(params1) != len(params2): raise AssertionError("Number of probabilities for '%s' and '%s' not equal"
                                                              % (state1.name, state2.name) )
        params1 = BayesianNetworkUtils._create_conditional_probability_dict(params1)
        params2 = BayesianNetworkUtils._create_conditional_probability_dict(params2)
        for key in params1.keys():
            if not params2.has_key(key):
                raise AssertionError("Conditions for '%s' and '%s' not equal" % (state1.name, state2.name))

    @staticmethod
    def _create_conditional_probability_dict(items):
        out = {}
        for item in items:
            key = ''
            for i in item[0:-1]:
                key += str(i) + '_'
            out[key] = key
        return out

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
#
# state1=[]
# state1.append([1,2,3,4])
# state1.append([6,2,3,4])
# state1.append([3,8,3,4])
# state2=[]
# state2.append([1,2,3,4])
# state2.append([3,8,3,4])
# state2.append([6,2,3,4])
#
# BayesianNetworkUtils._assert_conditional_probability_table_structures_equality(state1, state2)