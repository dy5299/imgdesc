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

class ImgdescDB(models.Model):
    img_no = models.AutoField(primary_key=True, blank=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
#    userid = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING) #이걸로하면 column선택 못해서..우선위에로
    photo = models.ImageField(upload_to="%Y/%m/%d")
    caption = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def _str__(self):   #객체의 문자열 표현 메소드
        return self.caption

#    class Meta:
#        db_table = 'imgdesc_list'  #setting the db name. default value: myapp_modelName