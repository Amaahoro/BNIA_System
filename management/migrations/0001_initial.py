# Generated by Django 4.2.4 on 2023-08-15 21:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female')], default='', max_length=10, verbose_name='Gender')),
                ('nationality', models.CharField(max_length=50, verbose_name='Nationality')),
                ('nid_number', models.CharField(blank=True, max_length=50, unique=True, verbose_name='National ID Number')),
                ('birthdate', models.DateField(verbose_name='Birthdate')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='citizen/images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Image')),
                ('createdDate', models.DateField(auto_now_add=True, verbose_name='Created Date')),
            ],
        ),
        migrations.CreateModel(
            name='Colline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colline_name', models.CharField(max_length=50, unique=True, verbose_name='Colline Name')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_name', models.CharField(max_length=50, unique=True, verbose_name='Province Name')),
            ],
        ),
        migrations.CreateModel(
            name='LostIDCardReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=20, verbose_name='Lost Card ID number')),
                ('date_lost', models.DateField(verbose_name='When lost')),
                ('description', models.TextField(verbose_name='Description')),
                ('contact_info', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Contact Info')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Created Date')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lost_reports', to='management.citizen', verbose_name='Citizen')),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IDCardRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='registration/citizen/images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Citizen Image')),
                ('signature', models.BinaryField()),
                ('data_hash', models.BinaryField()),
                ('registration_date', models.DateField(auto_now_add=True, verbose_name='Registration Date')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.citizen', verbose_name='Citizen')),
                ('resident_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrations', to='management.colline', verbose_name='Resident Address')),
            ],
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commune_name', models.CharField(max_length=50, unique=True, verbose_name='Commune Name')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communes', to='management.province', verbose_name='Province')),
            ],
        ),
        migrations.AddField(
            model_name='colline',
            name='commune',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collines', to='management.commune', verbose_name='Commune'),
        ),
        migrations.CreateModel(
            name='CitizenParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.CharField(choices=[('', 'Select Parent'), ('Father', 'Father'), ('Mother', 'Mother')], default='', max_length=10, verbose_name='Parent')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='Last Name')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='management.citizen', verbose_name='Citizen')),
            ],
        ),
        migrations.AddField(
            model_name='citizen',
            name='birth_place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.colline', verbose_name='Resident Address'),
        ),
    ]
