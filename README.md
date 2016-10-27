# Django session events

Generalization of [django.contrib.messages framework](https://docs.djangoproject.com/en/dev/ref/contrib/messages/)
which allows you to queue any data tied to user session.

This can be useful for example for analytics. E.g. passing *signup*, *purchase* events to Google Analytics.

## How to use

```python
import request_events

def signup_view(request):
    # ... do something ...
    request_events.add_event(request, 'analytics', {
        'cetegory': 'registration',
        'action': 'signup'
    })
    return request
```

## Note

I can't remember who's the author of this module. I just found it in my work dir. It would be good to save it somewhere.
