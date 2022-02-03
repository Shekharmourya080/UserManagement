from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user_id = models.AutoField(primary_key=True,db_column='user_id')
    gender = models.CharField(max_length= 100, db_column='gender')
    city = models.CharField(max_length=100, db_column='city')
    country = models.CharField(max_length=100, db_column='country', null=True)
    auth = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, db_column='auth_id')
    contact = models.BigIntegerField(null=True)
    image = models.ImageField(upload_to='images',null=True)
    objects = models.Manager()



    class Meta:
        db_table = 'profile'
        permissions=(
            ('manage_user','Can Create User'),
            ('view_user','Can view user')
        )









