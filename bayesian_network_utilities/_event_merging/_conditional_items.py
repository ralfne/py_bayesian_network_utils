from pomegranate.distributions.ConditionalProbabilityTable import ConditionalProbabilityTable
from pomegranate.distributions.DiscreteDistribution import DiscreteDistribution
import numpy as np

from _conditional_item import _ConditionalItem


class _ConditionalItems(object):
    def __init__(self, distribution=None):
        self._items = []
        self._is_conditional = None
        if distribution is not None:
            if isinstance(distribution, ConditionalProbabilityTable):
                params = distribution.parameters[0]
                for row in params:
                    item = _ConditionalItem(row, is_conditional=True)
                    self._items.append(item)
            elif isinstance(distribution, DiscreteDistribution):
                params = distribution.parameters[0]
                for key, value in params.iteritems():
                    row = [key, value]
                    item = _ConditionalItem(row, is_conditional=False)
                    self._items.append(item)
            else: raise NotImplementedError()
            self._is_conditional = self.get_is_conditional()

    def get_is_conditional(self):
        if len(self._items) == 0: return None
        for item in self._items:
            if self._is_conditional is None:
                self._is_conditional = item.get_is_conditional()
            else:
                if self._is_conditional != item.get_is_conditional():
                    raise ValueError('Inconsistency; conditional and non-conditional items mixed')
        return self._is_conditional

    def add_item(self, item):
        self._items.append(item)
        if item.get_is_conditional() != self.get_is_conditional():
            raise ValueError('Inconsistency; conditional and non-conditional items mixed')

    def __iter__(self):
        return self._items.__iter__()

    def __getitem__(self, i):
        return self._items.__getitem__(i)

    def extend(self, items):
        if isinstance(items, dict):
            for key, value in items:
                self.add_item(value)
        else:
            for value in items:
                self.add_item(value)

    def create_merged_conditional_item(self, event_merge_def):
        if self._is_conditional:
            out = self._create_merged_conditional_item(event_merge_def)
        else:
            out = self._create_merged_non_conditional_item(event_merge_def)
        return out

    def _create_merged_non_conditional_item(self, event_merge_def):
        v = []
        sums = []
        original_event = ''
        for item in self._items:
            sums.append(item.get_probability())
            original_event = item.get_outcome()
        p = float(np.sum(sums))
        if original_event in event_merge_def.get_events():
            v.append(event_merge_def.get_merged_event())
        else:
            v.append(original_event)
        v.append(p)
        out = _ConditionalItem(v, is_conditional=False)
        return out

    def _create_merged_conditional_item(self, event_merge_def):
        if self._items[0].get_outcome() in event_merge_def.get_events():
            out = self._create_merged_conditional_item_for_outcome_merge(event_merge_def)
        else:
            out = self._create_merged_conditional_item_for_conditional_merge(event_merge_def)
        return out

    def _create_merged_conditional_item_for_outcome_merge(self, event_merge_def):
        v =[]
        for c in self._items[0].get_conditions():
            v.append(c)
        v.append(event_merge_def.get_merged_event())
        sums = []
        for item in self._items:
            sums.append(item.get_probability())
        p = float(np.sum(sums))
        v.append(p)
        out = _ConditionalItem(v)
        return out

    def _create_merged_conditional_item_for_conditional_merge(self, event_merge_def):
        v =[]
        for c in self._items[0].get_conditions():
            if c in event_merge_def.get_events():
                v.append(event_merge_def.get_merged_event())
            else:
                v.append(c)
        v.append(self._items[0].get_outcome())
        sums = []
        for item in self._items:
            sums.append(item.get_probability())
        p = float(np.sum(sums)) / len(sums)
        v.append(p)
        out = _ConditionalItem(v)
        return out

    def export_probabilities(self, parents=None):
        if self._is_conditional:
            probs = []
            for item in self._items:
                probs.append(item.export_probabilities())
            out = ConditionalProbabilityTable(probs,parents)
        else:
            probs={}
            for item in self._items:
                probs[item.get_outcome()] = item.get_probability()
            out = DiscreteDistribution(probs)
        return out

    # def outcome_or_conditions_exists_in_all_items(self, name):
    #     for item in self._items:
    #         if not item.exists_in_outcome_or_conditions(name): return False
    #     return True

    def __str__(self):
        out = ''
        for item in self._items:
            out += str(item) + ';'
        return out[0:-1]