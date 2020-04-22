from django import forms
from .models import ImgdescDB

class todoModelForm(forms.ModelForm):
	class Meta:
		model=ImgdescDB
        fields = ('')