from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_home),
    path('about/', views.get_about),
    path('menu/', views.get_menu),
    path('contact/', views.get_contact),
    path('blog/', views.get_blog),
    path('api/contact_me', views.contact_me)
]
