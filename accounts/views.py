from django.http import HttpResponse


def home(request):
    return HttpResponse("IMS skeleton is live")
