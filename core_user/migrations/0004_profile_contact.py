# Generated by Django 3.0.14 on 2022-01-31 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_user', '0003_auto_20220131_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contact',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
