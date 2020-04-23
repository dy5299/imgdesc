from django.urls import path, include
from . import views



app_name = 'imgdesc'

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('list/', views.ListView.as_view()),
    path('<int:pk>/<mode>/', views.BoardView.as_view(), name='board'),
#    path('accounts/', include('accounts.urls', namespace='accounts')),
#    path('account/', include('django.contrib.auth.urls')),
]

