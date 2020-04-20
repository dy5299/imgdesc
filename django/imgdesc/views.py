from django.shortcuts import render, redirect

from django.views import View
from django.views import generic

# Create your views here.
class Imgdesc_main(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'imgdesc_main/index.html'
        return render(request, template_name)