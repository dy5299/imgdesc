from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.views import View
from .forms import UserForm

class SignupView(View):
    def get(self, request):
        form = UserForm()
        return render(request, "accounts/signup.html", {'form':form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('index')



class SigninView(View):
    def get(self, request):
        return render(request, "accounts/signin.html")

    def post(self, request):
        #Loging 처리
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
#        if user == None :
#            return redirect('signin')    #urls.py에서 지정한 name. NOT 경로명.
        #로그인 성공한 경우
        login(request,user)
        return redirect('index')

class SignoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')