"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import imgdesc.views
#import accounts.views      #나중에 필요하면 써

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', imgdesc.views.IndexView.as_view(), name='index'),
#    path('index', IndexView.as_view()),
#    path('home/', IndexView.as_view()),

    path('imgdesc/', include('imgdesc.urls')),
    path('accounts/', include('accounts.urls')),
]

from django.conf.urls.static import static
from django.conf import settings
#개발환경에서의 media 파일 서빙
#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
