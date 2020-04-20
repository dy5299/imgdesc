from django.db import models

# Create your models here.
class Imgdesc(models.Model):
    user = models.CharField(max_length=20, blank=False)
    created_date = models.DateField(null=True, blank=True)

