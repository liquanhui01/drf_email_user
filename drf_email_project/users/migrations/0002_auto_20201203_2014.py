# Generated by Django 3.1.4 on 2020-12-03 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailuser',
            name='password',
            field=models.CharField(blank=True, max_length=50, verbose_name="user's password"),
        ),
    ]