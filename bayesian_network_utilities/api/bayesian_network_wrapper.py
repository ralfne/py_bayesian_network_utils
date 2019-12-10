from bayesian_network_utilities._event_merging._bayesian_network_merger import _BayesianNetworkMerger
from bayesian_network_utilities._event_merging._marginals_parser import _MarginalsParser
import pomegranate as pg


class BayesianNetworkWrapper(object):
    def __init__(self, pomegranate_bayesian_network):
        if not isinstance(pomegranate_bayesian_network, pg.BayesianNetwork):
            raise NotImplementedError()
        self._network = pomegranate_bayesian_network
        self._marginals_parser = _MarginalsParser(self._network)

    def get_marginals(self, statename):
        out = self._marginals_parser.get_marginals(statename)
        return out

    def merge_events(self, distribution_merge_defs, bake=True):
        merger = _BayesianNetworkMerger(distribution_merge_defs)
        out = merger.create_merged_bayesian_network()
        if bake: out.bake()
        return out