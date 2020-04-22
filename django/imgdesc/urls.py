from django.conf.urls import url, include
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'imgdesc'

urlpatterns = [
    path('', views.IndexView.as_view()),
]
