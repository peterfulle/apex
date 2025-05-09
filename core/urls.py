from django.urls import path
from .views import IndexView, contact_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact/', contact_view, name='contact'),
]