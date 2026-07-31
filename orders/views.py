from django.http import HttpResponse

def order_list(request):
    return HttpResponse("Orders Page")