# Generated by Django 4.2.3 on 2023-07-25 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone2',
        ),
    ]
