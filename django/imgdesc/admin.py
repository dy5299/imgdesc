from django.contrib import admin

# Register your models here.
from imgdesc.models import ImgdescDB

@admin.register(ImgdescDB)
class ImgdescDBAdmin(admin.ModelAdmin):
    list_display = ('img_no','userid','url','caption','created_date')

