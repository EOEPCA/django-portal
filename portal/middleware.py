from .settings import TOKEN_ID_COOKIE
from django.utils.deprecation import MiddlewareMixin

class TokenCookieMiddleWare(MiddlewareMixin):
    """
    Middleware to set token cookie
    If user is authenticated and there is no cookie, set the cookie,
    If the user is not authenticated and the cookie remains, delete it
    """

    def process_response(self, request, response):
        #if user and no cookie, set cookie

        if request.user.is_authenticated and not request.COOKIES.get(TOKEN_ID_COOKIE):
            response.set_cookie(TOKEN_ID_COOKIE, request.session['oidc_id_token'])

        elif not request.user.is_authenticated and request.COOKIES.get(TOKEN_ID_COOKIE):
            #else if if no user and cookie remove user cookie, logout
            response.delete_cookie(TOKEN_ID_COOKIE)
        return response
