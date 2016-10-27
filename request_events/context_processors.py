from .api import get_events


def messages(request):
    """
    Returns a lazy 'events' context variable.
    """
    return {
        'events': get_events(request),
    }
