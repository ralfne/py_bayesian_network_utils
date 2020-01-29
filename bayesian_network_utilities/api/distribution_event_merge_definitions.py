import pomegranate as pg
from pomegranate import ConditionalProbabilityTable, DiscreteDistribution
from bayesian_network_utils import BayesianNetworkUtils


class DistributionEventMergeDefinitions(object):
    ERR_DUPLICATE_EVENT_MSG = 'The same event is encoded multiple times.'
    ERR_DIST_NAME_NOT_FOUND_MSG = 'DistributionEventMergeDefinitions distribution name not found in network.'
    ERR_EVENT_NOT_FOUND = 'DistributionEventMergeDefinitions event not found in network distribution.'
    ERR_UNSPECIFIED_EVENTS_NOT_ALLOWED_MSG = 'Unspecified events not allowed'
    ERR_ONLY_ONE_MERGE_DEF_ALLOWED_MSG = 'Unspecified events allowed; therefor only one EventMergeDefinition is allowed'
    ERR_NETWORK_HAS_DUPLICATED_EVENT_NAMES = 'Assumption violation: network contains duplicated events (possibly across states)'

    def __init__(self, root_state_name, bayesian_network, allow_unspecified_events=False, assert_merge_definitions=False):
        if not isinstance(bayesian_network, pg.BayesianNetwork):
            raise NotImplementedError()
        unique = BayesianNetworkUtils.all_event_names_are_unique(bayesian_network)
        if not unique: raise ValueError(self.ERR_NETWORK_HAS_DUPLICATED_EVENT_NAMES)
        self._root_state_name = root_state_name
        self._allow_unspecified_events = allow_unspecified_events
        self._items = []
        self._bayesian_network = bayesian_network
        self._assert_merge_definitions = assert_merge_definitions

    def _assert_merge_defs(self):
        if self._allow_unspecified_events:
            if len(self._items) > 1: raise ValueError(self.ERR_ONLY_ONE_MERGE_DEF_ALLOWED_MSG)
        state = BayesianNetworkUtils.get_state(self._bayesian_network, self._root_state_name)
        if state is None: raise ValueError(self.ERR_DIST_NAME_NOT_FOUND_MSG)
        dist = state.distribution
        events = {}
        defined_events = 0
        for merge_def in self._items:
            for event in merge_def.get_events():
                defined_events += 1
                if events.has_key(event): raise ValueError(self.ERR_DUPLICATE_EVENT_MSG)
                events[event] = event
                if isinstance(dist, ConditionalProbabilityTable):
                    e = None
                    for p in dist.parameters[0]:
                        if event in p:
                            e = p
                            break
                elif isinstance(dist, DiscreteDistribution):
                    e = dist.parameters[0].get(event)
                if e is None:
                    raise ValueError(self.ERR_EVENT_NOT_FOUND)
        if not self._allow_unspecified_events:
            if not self._all_dist_events_are_specified(dist):
                raise ValueError(self.ERR_UNSPECIFIED_EVENTS_NOT_ALLOWED_MSG)

    def _all_dist_events_are_specified(self, dist):
        if isinstance(dist, ConditionalProbabilityTable):
            e = None
            for p in dist.parameters[0]:
                if not self._event_exists_in_merge_defs(p): return False
        elif isinstance(dist, DiscreteDistribution):
            for key, value in dist.parameters[0].iteritems():
                if not self._event_exists_in_merge_defs([key]): return False
        return True

    def _event_exists_in_merge_defs(self, dist_events):
        for merge_def in self._items:
            for event in merge_def.get_events():
                if event in dist_events: return True
        return False

    def get_bayesian_network(self):
        return self._bayesian_network

    def get_allow_unspecified_events(self):
        return self._allow_unspecified_events

    def get_root_state_name(self):
        return self._root_state_name

    def set_merge_definitions(self, merge_definitions):
        self._items = []
        self._items.extend(merge_definitions)
        if self._assert_merge_definitions: self._assert_merge_defs()

    def get_events(self):
        out = []
        for merge_def in self._items:
            out.extend(merge_def.get_events())
        return out

    def get_merged_eventnames(self):
        out = {}
        for merge_def in self._items:
            out[merge_def.get_merged_event()] = merge_def.get_merged_event()
        return out

    def __iter__(self):
        return self._items.__iter__()

    def __getitem__(self, i):
        return self._items[i]

