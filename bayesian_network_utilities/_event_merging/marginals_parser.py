from pomegranate import DiscreteDistribution, ConditionalProbabilityTable

class MarginalsParser(object):
    def __init__(self, pomgranate_bayesian_network):
        self._pomgranate_bayesian_network = pomgranate_bayesian_network
        self._items = {}
        #self._get_marginals_for_events(pomgranate_bayesian_network)
        statenames_events = self._map_statenames_to_events()
        self._assert_statenames_events_validity(statenames_events)
        self._events_statenames = self._create_events_statenames(statenames_events)

    def _map_statenames_to_events(self):
        out = {}
        for state in self._pomgranate_bayesian_network.states:
            name = state.name
            s = out.get(name, None)
            if s is None:
                s = {}
                out[name] = s
            dist = state.distribution
            if isinstance(dist, DiscreteDistribution):
                for key, value in dist.parameters[0].iteritems():
                    s[key] = key
            elif isinstance(dist, ConditionalProbabilityTable):
                for value in dist.parameters[0]:
                    s[value[-2]] = value[-2]
            else: raise NotImplementedError()
        return out

    def _assert_statenames_events_validity(self, event_statenames):
        eventnames = {}
        for key, value in event_statenames.iteritems():
            for ev_key, ev_value in value.iteritems():
                if eventnames.has_key(ev_key): raise ValueError('event_statenames assumption violiated')
                eventnames[ev_key] = ev_key

    def _create_events_statenames(self, statenames_events):
        out = {}
        for statename, state in statenames_events.iteritems():
            for ev_key, ev_value in state.iteritems():
                out[ev_key] = statename
        return out


    def get_marginals(self, state_name):
        out = self._items.get(state_name, None)
        if out is None:
            self._init_marginal_items()
            out = self._items.get(state_name, None)
        return out

    def _init_marginal_items(self):
        all_marginals = self._pomgranate_bayesian_network.marginal()
        for m in all_marginals:
            dist = m.parameters[0]
            item = {}
            last_event = None
            for key, value in dist.iteritems():
                item[key] = value
                last_event = key
            statename = self._events_statenames.get(last_event)
            self._items[statename] = item

    # def _get_marginals_for_events(self, pomgranate_bayesian_network):
    #     all_marginals = pomgranate_bayesian_network.marginal()
    #     for m in all_marginals:
    #         nickname = self._get_nickname_for_event_marginals(m)
    #         self._items[nickname] = m.parameters[0]
    #
    # def _get_nickname_for_event_marginals(self, event_marginals):
    #     for key, value in event_marginals.parameters[0].iteritems():
    #         i = key.find(':')
    #         out = key[0:i]
    #         return out
    #
    # def get_as_list(self, nickname):
    #     out = []
    #     item = self._items.get(nickname)
    #     for key, value in item.iteritems():
    #         row = []
    #         row.append(key)
    #         row.append(value)
    #         out.append(row)
    #     return out