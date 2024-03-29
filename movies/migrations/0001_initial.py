# Generated by Django 3.1.3 on 2020-11-26 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('original_title', models.CharField(max_length=100)),
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
        migrations.CreateModel(
            name='LikeMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_movie', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
