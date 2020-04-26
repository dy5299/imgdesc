from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import ImgdescDB

from django.views import View
from django.views import generic
from django.http import HttpResponse

from django.forms import Form, CharField, Textarea, ValidationError
from .forms import PostForm

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
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
        return render(request, template_name, {'user': request.user, 'mydb': mydb})


class ListView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        #        username = request.session['username']  # text
        #        user = User.objects.get(username=username)  # object
        #        mydb = ImgdescDB.objects.all().filter(userid=request.user)
        mydb = ImgdescDB.objects.select_related('userid').all().order_by('-img_no')
        # pagination
        page = request.GET.get('page', 1)
        p = Paginator(mydb, 10)  # collection 형태의 데이터면 상관 없다 / page 당 개수
        mydb_sub = p.page(page)

        #        ImgdescDB.objects.create()
        #        print(mydb.photo.url)

        return render(request, 'imgdesc/list.html', {'mydb': mydb_sub})  # 리턴에 'user': request.user 지움.for templatetags
        # return render(request, "imgdesc/list.html", {'username': username, 'mydb': mydb})



class tts(View):
    def post(self, request, pk):
#        user = request.user  # 로그인한 유저를 가져온다.
#        img_no = request.POST.get('pk', None)
        img_no = pk
        mypost = ImgdescDB.objects.get(pk=img_no)  # 해당 오브젝트를 가져온다.

        # tts
        from gtts import gTTS
        tts = gTTS(text=mypost.caption_ko, lang='ko')
        myvoicepath = os.path.splitext(mypost.photo.path)[0] + '.mp3'
        myvoicepath = myvoicepath.replace('\\','/')
        tts.save(myvoicepath)
        message = '음성안내를 시작합니다'
        #DB저장
        myvoiceurl = '/media/' + myvoicepath.split('media/')[-1]
        mypost.audio_url = myvoiceurl
        mypost.save()
        context = {'myvoiceurl': myvoiceurl, 'message': message}
        return JsonResponse(context)
        # dic 형식을 json 형식으로 바꾸어 전달한다.



class ListajaxView():
    def get(self, request, pk):
        mydb = get_object_or_404(ImgdescDB, pk=pk)
        voice_filename = mydb.photo.split('.')[:-1]
        voice_filename = "".join(voice_filename) + '.mp3'
        data = {
            'img_no': mydb.img_no,
            'cap_txt': mydb.caption_ko,
            'voice': voice_filename,
        }
        return JsonResponse({'data': data})

    def post(self, request):
        if self.request.is_ajax():
            mydb = ImgdescDB.objects.all()
            text = self.request.POST['message']
            return JsonResponse({})



class BoardView(LoginRequiredMixin, View):
    #    login_url = '/accounts/signin/'
    def get(self, request, pk, mode):  # 특정 포스트를 수정하므로 pk parameter를 받아와야 한다.
        if mode == 'detail':
            p = get_object_or_404(ImgdescDB, pk=pk)  # 에러나면 아래 return이 아닌, pagenotfound(404) exception로 리턴시킨다.
            return render(request, "imgdesc/detail.html", {"d": p})
        elif mode == 'add':
            form = PostForm()  # empty form
            return render(request, "imgdesc/edit.html", {'form': form})
        elif mode == 'edit':
            post = get_object_or_404(ImgdescDB, pk=pk)
            form = PostForm(instance=post)  # instance라는 parameter에 model data(post) 넣음
            return render(request, "imgdesc/edit.html", {'form': form})
        elif mode == 'del':
            post = get_object_or_404(ImgdescDB, pk=pk)
            post.delete()
            return redirect('/imgdesc/list')
        else:
            return HttpResponse("error page")

    def post(self, request, pk, mode='edit'):
        #        username = request.session["username"]
        #       userid = User.objects.get(username=username)

        # 글쓰기에서 submit 시
        if pk == 0:
            author = ImgdescDB.objects.create(userid=request.user)  # user id는 폼 이전에 미리 채움. NOT NULL이라서
            form = PostForm(request.POST, request.FILES, instance=author)  # 받은 데이터로 폼 채움



        # 수정에서 submit 시
        else:
            post = get_object_or_404(ImgdescDB, pk=pk)
            form = PostForm(request.POST, request.FILES, instance=post)

        # 폼 유효성 검사
        if form.is_valid():
            post = form.save(commit=False)

            if pk == 0:  # 글쓰기 시
                pho = request.FILES.get('photo')
                uploaded_image = ImgdescDB(photo=pho)

                import datetime
                today = datetime.date.today()
                myphotodir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                          'media') + '{/%Y%m/%d/}'.format(today)
                myphotourl = myphotodir + uploaded_image.photo.url.split('/')[-1]
                captioning_result = run_captioning(myphotourl)
                captioning_result_ko = translation(captioning_result)
                #                captioning_result = testimport('testing')
                post.caption_en = captioning_result
                post.caption_ko = captioning_result_ko

                #                post.userid = request.user      #유효성 한 다음에 다시 user 넣는건가.. 위와 중복이라 뺌.
                post.save()  # form data로부터 post data(model data)를 얻기 위해서 save. NOT for save.
                '''
                # tts
                from gtts import gTTS
                tts = gTTS(text=captioning_result_ko, lang='ko')
                myvoiceurl = os.path.splitext(myphotourl)[0] + '.mp3'
                tts.save(myvoiceurl)
                '''

            else:
                post.publish()
            #            return redirect('/imgdesc/list')
            return JsonResponse({'status': 0, 'message': 'Uploaded Successfully'})
        else:
            #            return render(request, 'imgdesc/edit.html', {'form':form})
            return JsonResponse({'status': -1, 'message': 'Failed', 'errors': form.errors})


class TTSView(View):
    def get(self, request, pk):
        cap_txt = ImgdescDB.objects.get(img_no=pk).caption_ko
        captioning_result_ko = cap_txt.split('\t')[-1]

        myphotodir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  'media') + '{:/%Y%m/%d/}'.format(today)
        myphotourl = myphotodir + uploaded_image.photo.url.split('/')[-1]

        # tts
        from gtts import gTTS
        tts = gTTS(text=captioning_result_ko, lang='ko')
        myvoiceurl = os.path.splitext(myphotourl)[0] + '.mp3'
        tts.save(myvoiceurl)
        return render(request, 'imgdesc/TTSresult.html', {'myvoiceurl': myvoiceurl, 'mydb': mydb})



def ajaxdel(request):
    pk = request.GET.get('pk')
    post = ImgdescDB.objects.get(pk=pk)
    post.delete()
    return JsonResponse({'error': '0'})


def ajaxget(request):
    username = request.session["username"]
    user = User.objects.get(username=username)

    page = request.GET.get('page', 1)
    datas = ImgdescDB.objects.all().filter(useid=user, category='common')

    page = int(page)
    subs = datas[(page - 1) * 3:(page) * 3]
    '''p = Paginator(datas, 3)
    subs = p.page(page)'''

    datas = {'mydb': [{'pk': sub.pk, 'title': sub.title, 'cnt': sub.cnt} for sub in subs]}
    return JsonResponse(datas, json_dumps_params={'ensure_ascii': False})
    # 마지막 JsonResponse 뒤에 옵션은, json만 출력했을 때 한글이 제대로 보이도록 하는 옵션이다.
    # 자바스크립트가 알아서 인코딩하므로 없어도 상관 없다.
