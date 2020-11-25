from django.shortcuts import render, redirect, get_object_or_404
from .models import Genre, Movie, LikeMovie
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.paginator import Paginator
from accounts.forms import GenreChoiceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.views.decorators.http import require_POST
import requests
import json

# def home(request):
#     return render(request,'movies/home.html')

# Create your views here.
def genre_choice(request):
    user = request.user
    if request.method == 'POST':
        form = GenreChoiceForm(request.POST,instance=user)
        if form.is_valid():
            choice = form.save()
    return redirect('movies:index')



def index(request):
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    today = date.today()
    sevendays = today - timedelta(days=1)
    #movie_ids = LikeMovie.objects.filter(created_at__range=[sevendays,today]).values('movie_id').annotate(movie_count = Count('movie_id')).order_by('-movie_id')[::20]
    movie_ids = LikeMovie.objects.filter(created_at__range=[sevendays,today]).values('movie_id')
    
    
    #7일동안 좋아요한 영화보여주기
    weekly_recommend = []
    for i in movie_ids:
    
        weekly_recommend.append(Movie.objects.get(id=i['movie_id']))

    
    #유저가 좋아요한 영화와 비슷한 영화 추천
    API_KEY='48bad6a2dc7df8164930b0ed851e6d37'
    language = 'ko-KR'
    params = {'api_key':API_KEY, 'language':language}
    
    movie_ids_api = []
    for i in movie_ids:
        item=Movie.objects.filter(id=i['movie_id']).values()
        print(item,'dd')
        movie_ids_api.append(item[0]['movie_id'])

    similar_movies = []
    for movie_id in movie_ids_api:
        URL=f'https://api.themoviedb.org/3/movie/{movie_id}/similar'

        res = requests.get(URL, params=params)
        similar_items = res.json()['results']
        if len(similar_items) > 1:
            for i in range(15):
                similar_movies.append(similar_items[i])

    
    #장르별  추천
    recommend_movies2 = []
    if request.user.genre.count():
        user_genres = []
        movie_genres = request.user.genre.all()
        for i in movie_genres:
            user_genres.append(i.id)
        recommend_movies_genre = Movie.objects.filter(genres__id = user_genres[0])
        for i in user_genres[1:]:
            recommend_movies_genre = recommend_movies_genre|Movie.objects.filter(genres__id=i)
        recommend_movies2 = recommend_movies_genre.order_by('-vote_average').distinct()[:10]
    
    context = {

        'genres': genres,
        'movies': movies,
        'recommend_movies_days1': weekly_recommend[:10],
        'recommend_movies_days2': weekly_recommend[5:10],
        'recommend_movies_genre1': recommend_movies2[:5],
        'recommend_movies_genre2': recommend_movies2[5:10],
        'similar_movies':similar_movies,
    }

    return render(request, 'movies/index.html', context)



#출연진 추가, 리뷰톡톡 추가..
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_id = movie.movie_id
    User = get_user_model()

    if request.user.is_authenticated:
        user = get_object_or_404(User,username=request.user.username)

        
        API_KEY='48bad6a2dc7df8164930b0ed851e6d37'
        language = 'ko-KR'
        params = {'api_key':API_KEY, 'language':language}
        
        #비슷한 영화
        URL = f'https://api.themoviedb.org/3/movie/{movie_id}/similar'
        res = requests.get(URL, params = params)

        similar_items = res.json()['results']

        #출연진
        URL_2 = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
        res_2 = requests.get(URL_2,params=params)

        movie_credit = res_2.json()['cast']

        similar_movies = []
        actors = [] 
        for i in range(10):
            similar_movies.append(similar_items[i])
            actors.append(movie_credit[i])

    
        context = {
            'movie':movie,
            'similar_movies':similar_movies,
            'actors':actors,
        }
        return render(request, 'movies/movie_detail.html',context)
    else:
        return redirect('accounts:login')




def movie_like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.like.filter(pk=user.pk).exists():
        m1 = LikeMovie.objects.filter(user=user).filter(movie=movie)
        m1.delete()
        liked = False
    else:
        m1 = LikeMovie.objects.create(user=user,movie=movie)
        liked = True

    context = {
        'liked': liked,
        'count': movie.like.count(),
    }
    return JsonResponse(context)



def movie_list(request, genre_id):
    genre_movies = Movie.objects.filter(genres__id=genre_id)
    paginator = Paginator(genre_movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'genre_movies': genre_movies,
        'page_obj': page_obj,
    }
    return render(request, 'movies/movie_list.html', context)



def movie_search(request):
    movie_name = request.GET.get('movie_name', '')
    genre_movies = Movie.objects.filter(title__contains=movie_name)
    paginator = Paginator(genre_movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'genre_movies': genre_movies,
        'page_obj': page_obj,
    }
    return render(request, 'movies/movie_list.html', context)





