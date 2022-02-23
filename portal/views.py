
from django.shortcuts import render
from .settings import HOSTNAME, USER_PREFIX, AUTHHOST


def index(request):
    context = {'hostname': HOSTNAME, 'user_prefix': USER_PREFIX, 'login_prefix' : AUTHHOST}
    return render(request, 'index.html', context)