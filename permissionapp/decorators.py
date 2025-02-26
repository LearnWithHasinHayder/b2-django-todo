from functools import wraps
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

def group_required(*group_names):
    """
    A decorator that checks if a user belongs to specified groups.
    Usage example: @group_required('admins', 'editors')
    """
    # Check if user is in any of the required groups
    def is_in_groups(user):
        # First check if user is logged in
        if not user.is_authenticated:
            return False
        
        # Superuser always gets access
        if user.is_superuser:
            return True
        
        # Check if user belongs to any of the required groups
        for group in group_names:
            if user.groups.filter(name=group).exists():
                return True
        return False
    
    # The actual decorator
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(request, *args, **kwargs):
            # If user isn't in groups, deny access
            if not is_in_groups(request.user):
                raise PermissionDenied
            # If user is in groups, show the view
            return view_function(request, *args, **kwargs)
        return wrapped_view
    return decorator

def admin_required(view_func):
    return group_required('admins')(view_func)

def editor_required(view_func):
    return group_required('editors')(view_func)

def manager_required(view_func):
    return group_required('managers')(view_func)

def hasin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.username == 'hasin':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden('This page is only accessible by hasin')
    return _wrapped_view

