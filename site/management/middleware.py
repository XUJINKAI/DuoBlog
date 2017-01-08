#
# https://djangosnippets.org/snippets/1219/
#
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import re

class RequirePermissionMiddleware(MiddlewareMixin):
    """
    Middleware component that wraps the permission_check decorator around 
    views for matching URL patterns. To use, add the class to 
    MIDDLEWARE_CLASSES and define RESTRICTED_URLS and 
    RESTRICTED_URLS_EXCEPTIONS in your settings.py.
    
    For example:
    
    RESTRICTED_URLS = (
                          (r'/topsecet/(.*)$', 'auth.access_topsecet'),
                      )
    RESTRICTED_URLS_EXCEPTIONS = (
                          r'/topsecet/login(.*)$', 
                          r'/topsecet/logout(.*)$',
                      )
                      
    RESTRICTED_URLS is where you define URL patterns and their associated 
    required permissions. Each URL pattern must be a valid regex. 
    
    RESTRICTED_URLS_EXCEPTIONS is, conversely, where you explicitly define 
    any exceptions (like login and logout URLs).
    """
    def __init__(self, *args, **kwargs):
        self.restricted = tuple([(re.compile(url[0]), url[1]) for url in settings.RESTRICTED_URLS])
        self.exceptions = tuple([re.compile(url) for url in settings.RESTRICTED_URLS_EXCEPTIONS])
        super().__init__(*args, **kwargs)
        
    def process_view(self,request,view_func,view_args,view_kwargs):
        # An exception match should immediately return None
        for path in self.exceptions:
            if path.match(request.path): return None            
        # Requests matching a restricted URL pattern are returned 
        # wrapped with the permission_required decorator
        for rule in self.restricted:
            url, required_permission = rule[0], rule[1]
            if url.match(request.path): 
                return permission_required(required_permission)(view_func)(request,*view_args,**view_kwargs)             
        # Explicitly return None for all non-matching requests
        return None