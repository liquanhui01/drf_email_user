# Generated by Django 3.1.4 on 2020-12-04 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201203_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailuser',
            name='email',
            field=models.EmailField(max_length=255, verbose_name="user's email"),
        ),
    ]