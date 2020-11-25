# Generated by Django 3.1.3 on 2020-11-25 06:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('original_title', models.CharField(max_length=100)),
                ('release_date', models.DateField(max_length=50)),
                ('popularity', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('vote_average', models.FloatField()),
                ('adult', models.BooleanField()),
                ('overview', models.TextField()),
                ('original_language', models.CharField(max_length=100)),
                ('poster_path', models.CharField(max_length=500, null=True)),
                ('backdrop_path', models.CharField(max_length=100, null=True)),
                ('movie_id', models.IntegerField()),
                ('video', models.BooleanField()),
                ('genre_ids', models.ManyToManyField(related_name='movies', to='movies.Genre')),
                ('like', models.ManyToManyField(related_name='liker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]