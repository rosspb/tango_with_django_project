from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    #in views file the function is called index and that is why we call it below
    #we leave the first argument blank as we are calling index of rango app
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]