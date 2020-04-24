from django.shortcuts import render, redirect, get_object_or_404,HttpResponse,HttpResponseRedirect

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

        if user is None :
            return redirect('accounts:signin')
#            return HttpResponseRedirect('/')

        #로그인 성공한 경우
        if user is not None :
            login(request, user)
        return redirect('index')

class SignoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')
