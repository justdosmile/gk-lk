# Generated by Django 3.0.5 on 2020-04-06 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0004_auto_20200406_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressregistration',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Адрес регистрации'),
        ),
    ]