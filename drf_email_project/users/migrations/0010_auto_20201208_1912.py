# Generated by Django 3.1.4 on 2020-12-08 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_emailuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailuser',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='是否是管理员'),
        ),
    ]