from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import ImgdescDB

from django.views import View
from django.views import generic
from django.http import HttpResponse

from django.forms import Form, CharField, Textarea, ValidationError
from .forms import PostForm

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# captioning
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../captioning/')))
from test_oneimg import run_captioning, testimport, translation

# Create your views here.
class IndexView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        mydb = ImgdescDB.objects.all()
        print(mydb)

        template_name = 'imgdesc/index.html'
        return render(request, template_name, {'user': request.user,'mydb' : mydb})

class ListView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
#        username = request.session['username']  # text
#        user = User.objects.get(username=username)  # object
#        mydb = ImgdescDB.objects.all().filter(userid=request.user)
        mydb = ImgdescDB.objects.all().order_by('-created_date')
        # pagination
        page = request.GET.get('page', 1)
        p = Paginator(mydb, 10)  # collection 형태의 데이터면 상관 없다 / page 당 개수
        mydb_sub = p.page(page)

        return render(request, 'imgdesc/list.html', {'mydb' : mydb_sub})    #리턴에 'user': request.user 지움.for templatetags
        #return render(request, "imgdesc/list.html", {'username': username, 'mydb': mydb})



#@login_required
class BoardView(View):
    def get(self, request, pk, mode):     #특정 포스트를 수정하므로 pk parameter를 받아와야 한다.
        if mode == 'detail':
            p = get_object_or_404(ImgdescDB, pk=pk)  # 에러나면 아래 return이 아닌, pagenotfound(404) exception로 리턴시킨다.
            return render(request, "imgdesc/detail.html", {"d": p})
        elif mode == 'add' :
            form = PostForm()       #empty form
            return render(request, "imgdesc/edit.html", {'form': form})
        elif mode == 'edit' :
            post = get_object_or_404(ImgdescDB, pk=pk)
            form = PostForm(instance=post)      #instance라는 parameter에 model data(post) 넣음
            return render(request, "imgdesc/edit.html", {'form':form})
        elif mode == 'del' :
            post = get_object_or_404(ImgdescDB, pk=pk)
            post.delete()
            return redirect('/imgdesc/list')
        else :
            return HttpResponse("error page")


    def post(self, request, pk, mode='edit'):
#        username = request.session["username"]
 #       userid = User.objects.get(username=username)

        # 글쓰기에서 submit 시
        if pk == 0:
            author = ImgdescDB.objects.create(userid=request.user)              #user id는 폼 이전에 미리 채움. NOT NULL이라서
            form = PostForm(request.POST, request.FILES, instance=author)       #받은 데이터로 폼 채움



        # 수정에서 submit 시
        else:
            post = get_object_or_404(ImgdescDB, pk=pk)
            form = PostForm(request.POST, request.FILES, instance=post)

        #폼 유효성 검사
        if form.is_valid():
            post = form.save(commit=False)

            if pk == 0 :
                pho = request.FILES.get('photo')
                uploaded_image = ImgdescDB(photo=pho)

                mydir=uploaded_image.photo.url.split('/')
                import datetime
                today = datetime.date.today()
                mydir2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media') + '{:/%Y%m/%d/}'.format(today) + mydir[-1]
                captioning_result = run_captioning(mydir2)
#                captioning_result = testimport('testing')
                post.caption = captioning_result + '\t' + translation(captioning_result)

#                post.userid = request.user      #유효성 한 다음에 다시 user 넣는건가.. 위와 중복이라 뺌.
                post.save()         #form data로부터 post data(model data)를 얻기 위해서 save. NOT for save.


            else :
                post.publish()
#            return redirect('/imgdesc/list')
            return JsonResponse({'status': 0, 'message': 'Uploaded Successfully'})
        else:
#            return render(request, 'imgdesc/edit.html', {'form':form})
            return JsonResponse({'status': -1, 'message': 'Failed', 'errors': form.errors})







