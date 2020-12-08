# Generated by Django 3.1.4 on 2020-12-04 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20201204_1622'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailuser',
            old_name='is_verified',
            new_name='is_verify',
        ),
        migrations.RemoveField(
            model_name='emailuser',
            name='is_actived',
        ),
        migrations.AlterField(
            model_name='emailuser',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='是否激活'),
        ),
    ]