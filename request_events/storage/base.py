from __future__ import unicode_literals

from collections import defaultdict


class BaseStorage(object):
    """
    This is the base backend for temporary message storage.

    This is not a complete class; to be a usable storage backend, it must be
    subclassed and the two methods ``_get`` and ``_store`` overridden.
    """

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self._queued_events = defaultdict(list)
        super(BaseStorage, self).__init__(*args, **kwargs)

    def __getitem__(self, group):
        events = self._queued_events.pop(group, []) + self._loaded_events.pop(group, [])
        return events

    @property
    def _loaded_events(self):
        """
        Returns a list of loaded events, retrieving them first if they have
        not been loaded yet.
        """
        if not hasattr(self, '_loaded_data'):
            events, all_retrieved = self._get()
            self._loaded_data = events or []
        return self._loaded_data

    def _get(self, *args, **kwargs):
        """
        Retrieves a dol (dictionary of lists) of stored events. Returns a
        tuple of the events and a flag indicating whether or not all the
        events originally intended to be stored in this storage were, in
        fact, stored and retrieved; e.g., ``(events, all_retrieved)``.

        **This method must be implemented by a subclass.**

        If it is possible to tell if the backend was not used (as opposed to
        just containing no events) then ``None`` should be returned in
        place of ``events``.
        """
        raise NotImplementedError('subclasses of BaseStorage must provide a _get() method')

    def _store(self, events, response, *args, **kwargs):
        """
        Stores a dol (dictionary of lists) of events, returning a dol of any
        events which could not be stored.

        **This method must be implemented by a subclass.**
        """
        raise NotImplementedError('subclasses of BaseStorage must provide a _store() method')

    def update(self, response):
        """
        Stores all unread events.

        If the backend has yet to be iterated, previously stored events will
        be stored again. Otherwise, only events added after the last
        iteration will be stored.
        """
        events = merge_dols(self._loaded_events, self._queued_events)
        return self._store(events, response)

    def add(self, group, data):
        """
        Queues an event to be stored.
        """
        self._queued_events[group].append(data)


def merge_dols(dol1, dol2):
    """
    Merges two dols (dictionary of lists).
    """
    keys = set(dol1).union(dol2)
    no = []
    return dict((k, dol1.get(k, no) + dol2.get(k, no)) for k in keys)
