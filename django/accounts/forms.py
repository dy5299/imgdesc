from django import forms
#from .models import accounts   #이건 틀림. 여기에 model 정의 안 했잖아.
from django.contrib.auth.models import User

def validator(value):
    if len(value)<4 :
        raise ValidationError("너무 짧습니다.");


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email']

    def __init__(self, *args, **kwargs):                    #내 생성자 정의
        super(UserForm, self).__init__(*args, **kwargs)     #부모 생성자 호출
        self.fields['username'].validuserIDators = [validator]