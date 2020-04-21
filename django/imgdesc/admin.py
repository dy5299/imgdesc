from django.contrib import admin

# Register your models here.
from imgdesc.models import ImgdescList

@admin.register(ImgdescList)
class ImgdescListAdmin(admin.ModelAdmin):
    list_display = ('img_no','userid','url','caption','created_date')

