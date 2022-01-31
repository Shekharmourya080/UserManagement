from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user_id = models.AutoField(primary_key=True,db_column='user_id')
    gender = models.CharField(max_length= 100, db_column='gender')
    city = models.CharField(max_length=100, db_column='city')
    country = models.CharField(max_length=100, db_column='country')
    auth = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, db_column='auth_id')
    contact = models.BigIntegerField(max_length=10)
    objects = models.Manager()

    class Meta:
        db_table = 'profile'





