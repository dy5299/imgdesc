# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.utils import timezone
#from django.conf import settings
from django.contrib.auth.models import User

#for delete
import os
from django.conf import settings

class ImgdescDB(models.Model):
    img_no = models.AutoField(primary_key=True, blank=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
#    userid = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING) #이걸로하면 column선택 못해서..우선위에로
    photo = models.ImageField(upload_to="%Y%m/%d", null=False)
    caption_en = models.CharField(max_length=100, blank=True, null=True)
    caption_ko = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    audio = models.FileField(blank=True, null=True)

    def _str__(self):   #객체의 문자열 표현 메소드
        return self.caption_en

    def total_myphoto(self):
        return self.img_no.count()

'''
    # Delete overwriting 하면 파일이 ImgdescDB 객체 인스턴스와 함께 삭제될 것이다.
    def delete(self, *args, **kwargs):
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.path))
            super(ImgdescDB, self).delete(*args, **kargs)   #원래의 delete 함수를 실행
'''
#    class Meta:
#        db_table = 'imgdesc_list'  #setting the db name. default value: myapp_modelName