from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings




def index(request):
    #boldmessage matches to boldmessage in template
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    #then return rendered response
    return render(request, 'rango/index.html', context=context_dict)
    
def about(request):

    return render(request, 'rango/about.html')
