from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexForm.as_view, name='index_form')
]
