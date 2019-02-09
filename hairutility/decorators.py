from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponse
from django.conf import settings
import base64


class BasicAuthDecorator(object):

    def __init__(self, get_response):
        self.get_response = get_response

        # Handles authorization for accessing the site in beta
        # If DEBUG is true, we're in dev. Raise MiddlewareNotUsed to remove
        # this middleware from the list.
        # TODO: This should probably be based off of the QA env once we hit
        # production

        # if settings.DEBUG:
        #     raise MiddlewareNotUsed

    def _unauthed(self):
        AUTH_TEMPLATE = """ <html> <title>Authentication Required</title> <body> Sorry, we're not ready for you yet. </body> </html> """
        response = HttpResponse(AUTH_TEMPLATE, content_type="text/html")
        response['WWW-Authenticate'] = 'Basic realm="This site is currently open to beta-testers only"'
        response.status_code = 401
        return response
# Need to take BETA_Authorization off

    def __call__(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            # HTTTP BASIC not found
            return self._unauthed()
        else:
            authentication = request.META['HTTP_AUTHORIZATION']
            (auth_method, auth) = authentication.split(' ', 1)
            if 'basic' != auth_method.lower():
                return self._unauthed()
            auth = base64.b64decode(auth.strip()).decode('utf-8')
            username, password = auth.split(':', 1)
            if (
                username == settings.BASICAUTH_USERNAME and
                password == settings.BASICAUTH_PASSWORD
            ):
                return self.get_response(request)

            return self._unauthed()
