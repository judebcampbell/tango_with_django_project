from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from rango import views
from rango.forms import UserForm, UserProfileForm
from djano.urls import redirect
from djano.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

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
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(Category=categoy)
        context_dict['pages'] = pages
        context_dict['category'] = categoy
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context=context_dict)
@login_required
def add_category(request):
    form = CategoryForm()
    # A HTTP POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)
            # valid form?
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
   
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form' : form})
@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    #boolean to check if user is registered correctly
    register = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        #check validity of forms
        if user_Form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            #hash password then save
            user.set_password(user.set_password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            #if there is a picture request upload
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            
            registered = True
        
        else:
            #print problems to terminal
            print(user_form.errors, profile_form.errors)
    
    else:
        #render with 2 modelForm instances if not HTTP post
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render('rango/register.html', context = {'user_form': user_form, 'profile_form' : profile_form, 'registered' : registered})
    

def user_login(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse('Your Rango account is disabled.')
        
        else:
            print("invalid login detalis: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    else:
        return render(request, 'rango/login.html')

@login_required
def registered(request):
    return HttpResponse("Since you're logged in, you can see this text!")
    
