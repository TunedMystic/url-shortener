from functools import wraps

from django.core.exceptions import PermissionDenied


def link_owner(wrapped_function):
    '''
    A decorator to allow the owner of the Link to proceed.
    '''
    @wraps(wrapped_function)
    def wrapper(request, *args, **kwargs):
        key = kwargs.get('key')
        if not request.user.links.filter(key=key).exists():
            raise PermissionDenied
        return wrapped_function(request, *args, **kwargs)
    return wrapper
