# Generated by Django 3.1.3 on 2020-11-26 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='category',
        ),
    ]