from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('servicios/', views.services_view, name='services'),
    path('contacto/', views.ContactFormView.as_view(), name='contact'),
]
