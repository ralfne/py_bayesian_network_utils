from bayesian_network_utilities._event_merging._conditional_items import _ConditionalItems


class _ConditionalItemsMerger(object):
    def __init__(self, conditional_items, event_merge_definition):
        self._items = {}
        self._split_conditional_items(conditional_items, event_merge_definition)

    def _split_conditional_items(self, conditional_items, event_merge_definition):
        self._items = {}
        for item in conditional_items:
            item_signature = item.get_signature(event_merge_definition.get_events())
            split_items = self._items.get(item_signature, None)
            if split_items is not None:
                pass
            else:
                split_items = _ConditionalItems()
                self._items[item_signature] = split_items
            split_items.add_item(item)

    def iteritems(self):
        return self._items.iteritems()

    def create_merged_items(self, event_merge_def):
        out = _ConditionalItems()
        for key, value in self._items.iteritems():
            item = value.create_merged_conditional_item(event_merge_def)
            out.add_item(item)
        return out
