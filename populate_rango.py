import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django 
django.setup()
from rango.models import Category, Page

def populate():
    #first create a list of dictionariy containg pages 
    #want to add into each category
    #then create dictionary of dictionary for categories
    #allows iteration

    python_pages = [
        {'title' : 'Offical Python Tutorial',
        'url' : 'https://docs.python.org/3/tutorial/'},
        {'title' :'How to Think Like a Computer Scientist', 
        'url' : 'http://www.greenteapress.com/thinkpython/'},
        {'title' : 'Learn Python in 10 Minutes',
        'url' : 'http://www.korokitakis.net/tutorials/python'}
    ]
    
    django_pages = [
        {'title' : 'Official Django Tutorial',
        'url' : 'http://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title' : 'Djano Rocks',
        'url' : 'http://djanorocks.com/'},
        {'title' : 'How to Tango with Djano',
        'url' : 'http://www.tangowithdjan.com/'}
        ]

    other_pages = [
        {'title' : 'Bottle',
        'url' : 'http://bottlepy/org/docs/dev/'},
        {'title' : 'Flask',
        'url' : 'http://flask.pocoo.org'}
    ]

    cats = {'Python' : {'pages' : python_pages, 'views' : 128, 'likes' : 64},
        'Django' : {'pages' : django_pages, 'views' : 64, 'likes' : 32},
        'Other Frameworks' : {'pages' : other_pages, 'views' : 32, 'likes' : 16}
        }
        
    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_page(c,p['title'], p['url'])
    
    for c in Category.objects.all():
        for p in Page.objects.filter(Category=c):
            print(f' {c}: {p}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(Category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return Page

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
