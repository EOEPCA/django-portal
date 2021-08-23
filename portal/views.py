from django.views.generic import View
from django.http import HttpResponse

class HelloWordView(View):
    def get(self, request):
        return HttpResponse(
            "Helloword!"
        )
