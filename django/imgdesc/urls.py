from django.urls import path
from . import views



app_name = 'imgdesc'

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('list/', views.ListView.as_view(), name='list'),
    path('list/ajax/<int:pk>/', views.ListajaxView, name='listajax'),
    path('<int:pk>/<mode>/', views.BoardView.as_view(), name='board'),
    path('<int:pk>/voice/', views.TTSView, name='tts')
]

