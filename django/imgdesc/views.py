from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ImgdescDB

from django.views import View
from django.views import generic
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.forms import Form, CharField, Textarea, ValidationError


# Create your views here.
class IndexView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        mydb = ImgdescDB.objects.all()
        print(mydb)

        template_name = 'imgdesc_main/index.html'
        return render(request, template_name, {'user': request.user,'mydb' : mydb})



class LoginView(generic.View):
    def get(self, request):
        return render(request, "imgdesc_main/login.html")

    def post(self, request):
        #Loging 처리
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user == None :
            return redirect('login')    #urls.py에서 지정한 name. NOT 경로명.

        #로그인 성공한 경우
        request.session['username'] = username
        return redirect('index')












