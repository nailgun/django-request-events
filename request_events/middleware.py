from django.conf import settings
from .storage import default_storage


class RequestEventsMiddleware(object):
    """
    Middleware that handles temporary events.
    """

    @staticmethod
    def process_request(request):
        request._events = default_storage(request)

    @staticmethod
    def process_response(request, response):
        """
        Updates the storage backend (i.e., saves the events).

        If not all events could not be stored and ``DEBUG`` is ``True``, a
        ``ValueError`` is raised.
        """
        # A higher middleware layer may return a request which does not contain
        # messages storage, so make no assumption that it will be there.
        if hasattr(request, '_events'):
            # noinspection PyProtectedMember
            unstored_events = request._events.update(response)
            if unstored_events and settings.DEBUG:
                raise ValueError('Not all temporary events could be stored.')
        return response
