# Generated by Django 3.1.5 on 2021-02-09 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210208_0054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='category',
            new_name='categories',
        ),
    ]