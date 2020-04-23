from django import forms
from .models import ImgdescDB

def validator(value):
    if value.split('.')[-1] not in ['jpg','jpeg','png','bmp'] :
        raise ValidationError("jpg, jpeg, png, bmp 그림 파일을 지원합니다.");


class PostForm(forms.ModelForm):
    #    title = CharField(label='제목', max_length=20, validators=[validator])
    #    text = CharField(label='내용', widget=Textarea)
    class Meta:
        model = ImgdescDB    #model은 쟝고가 정의한 것. 에다 model data를 넣어준다
        fields = ['photo']      #가져올 fields만 선택 가능하다. 'created_date','userid',
#        fields = '__all__'

    def __init__(self, *args, **kwargs):                    #내 생성자 정의
        super(PostForm, self).__init__(*args, **kwargs)     #부모 생성자 호출
        self.fields['photo'].validuserIDators = [validator]