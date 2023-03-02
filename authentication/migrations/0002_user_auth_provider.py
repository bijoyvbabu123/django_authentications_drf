# Generated by Django 4.1.7 on 2023-03-01 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(choices=[('email', 'email'), ('google', 'google')], default='email', max_length=50, verbose_name='authentication provider'),
        ),
    ]