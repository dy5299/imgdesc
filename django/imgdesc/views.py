from django.shortcuts import render, redirect
from .models import ImgdescList

from django.views import View
from django.views import generic

# Create your views here.
class Imgdesc_main(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        mydb = ImgdescList.objects.all()
        print(mydb)

        template_name = 'imgdesc_main/index.html'
        return render(request, template_name, {'mydb' : mydb})