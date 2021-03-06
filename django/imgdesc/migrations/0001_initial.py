# Generated by Django 3.0.5 on 2020-04-23 02:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImgdescDB',
            fields=[
                ('img_no', models.AutoField(primary_key=True, serialize=False)),
                ('photo', models.ImageField(upload_to='')),
                ('caption', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('userid', models.ForeignKey(db_column='userID', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
