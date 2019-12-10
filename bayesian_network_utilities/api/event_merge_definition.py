class EventMergeDefinition(object):
    def __init__(self, merged_event_name):
        self._merged_event_name = merged_event_name
        self._items = []

    def add(self, event):
        self._items.append(event)

    def extend(self, events):
        self._items.extend(events)

    def get_events(self):
        return self._items

    def get_merged_event(self):
        return self._merged_event_name
