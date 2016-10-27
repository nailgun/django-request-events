from django.http import HttpRequest


class RequestEventFailure(Exception):
    pass


def add_event(request, group, data, fail_silently=False):
    """
    Attempts to add an event to the request using the 'request_events' app.
    """
    if not isinstance(request, HttpRequest):
        raise TypeError("add_event() argument must be an HttpRequest object, "
                        "not '%s'." % request.__class__.__name__)
    if hasattr(request, '_events'):
        # noinspection PyProtectedMember
        return request._events.add(group, data)
    if not fail_silently:
        raise RequestEventFailure('You cannot add events without installing '
                                  'request_events.middleware.RequestEventsMiddleware')


def get_events(request, group):
    """
    Returns the event storage on the request if it exists, otherwise returns
    an empty list.
    """
    if hasattr(request, '_events'):
        # noinspection PyProtectedMember
        return request._events
    else:
        return []
