from django.urls import path
from rango import views

app_name = 'rango'
urlpatterns = [
path('', views.index, name='index'),
#Ch3 exercise 1
path('about/', views.about, name='about'),
]
