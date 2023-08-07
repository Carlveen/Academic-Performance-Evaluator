from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class SessionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith('/admin'):
            response.set_cookie(
                settings.SESSION_COOKIE_NAME_ADMIN,
                request.session.session_key
            )
        else:
            response.set_cookie(
                settings.SESSION_COOKIE_NAME_WEBSITE,
                request.session.session_key
            )
        return response
