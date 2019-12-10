import pomegranate as pg
from pomegranate.distributions import DiscreteDistribution, ConditionalProbabilityTable


class BayesianNetworkUtils(object):

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