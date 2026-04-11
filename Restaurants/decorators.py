from functools import wraps
from django.core.exceptions import PermissionDenied

from .Services import isOwner, isStaff

def restrict_access(view_func):
    print("I am here")
    # @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        print("I am here in _wrapped")
        user = request.user
        
        if not user.is_authenticated:
            raise PermissionDenied
        
        elif (not isStaff(user)) and (not isOwner(user)):
            raise PermissionDenied
        
        else:
            print("survived both in _wrapped", user.is_authenticated, isStaff(user), isOwner(user))

            return view_func(request, *args, **kwargs)

    return _wrapped

