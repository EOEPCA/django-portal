
from django.shortcuts import render
from .settings import HOSTNAME, USER_PREFIX


def index(request):
    context = {'hostname': HOSTNAME, 'user_prefix': USER_PREFIX}
    return render(request, 'index.html', context)