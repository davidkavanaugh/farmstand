# Generated by Django 2.2.4 on 2020-11-04 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign_up', '0009_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default='', max_length=255),
        ),
    ]
