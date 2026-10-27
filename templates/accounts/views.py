from django.http import HttpResponse
def home(request):
    if not request.user.is_authenticated:
        return HttpResponse("Please log in at /login/")
    return HttpResponse(f"Hello {request.user.display_name}, role: {request.user.role}")
