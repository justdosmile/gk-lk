# Generated by Django 3.0.5 on 2020-04-06 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200406_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressregistration',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.Profile', verbose_name='Адрес регистрации'),
        ),
    ]