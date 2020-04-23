from django.urls import path
from . import views



app_name = 'imgdesc'

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('list/', views.ListView.as_view(), name='list'),
    path('<int:pk>/<mode>/', views.BoardView.as_view(), name='board'),
]

