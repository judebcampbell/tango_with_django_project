from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rango.models import Category, Page




def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    #then return rendered response
    return render(request, 'rango/index.html', context=context_dict)
    
def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    #create context dictionary
    context_dict = {}
    
    try:
        cat = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(Category=cat)

        context_dict['pages'] = pages
        context_dict['category'] = cat
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context=context_dict)
