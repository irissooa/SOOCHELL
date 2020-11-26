from django.shortcuts import render, redirect, get_object_or_404
from .models import Genre, Movie, LikeMovie
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.paginator import Paginator
# from accounts.forms import GenreChoiceForm
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
    # movie_ids = LikeMovie.objects.filter(created_at__range=[sevendays,today]).values('movie_id')
    
    user_pk = request.user.pk
    user_movie = Movie.objects.filter(like=user_pk).values('movie_id')
    print(user_movie,'유저가 좋아요한 무비들')
    movie_ids=[]
    for i in user_movie:
        movie_ids.append(i.get('movie_id'))
    print(movie_ids)
    #7일동안 좋아요한 영화보여주기
    weekly_recommends = []
    for i in movie_ids:
        weekly_recommends.append(Movie.objects.get(movie_id=i))
        # weekly_recommends.append(Movie.objects.get(id=i['movie_id']))
    print(weekly_recommends)
    #유저가 좋아요한 영화와 비슷한 영화 추천
    API_KEY='48bad6a2dc7df8164930b0ed851e6d37'
    language = 'ko-KR'
    params = {'api_key':API_KEY, 'language':language}
    
    movie_ids_api = []
    for i in movie_ids:
        item=Movie.objects.filter(movie_id=i).values()
        # print(item,'뭐니')
        movie_ids_api.append(item[0]['movie_id'])
    print(movie_ids_api,'이건어아란ㅇㄹ')
    similar_movies = []
    for movie_id in movie_ids_api:
        URL=f'https://api.themoviedb.org/3/movie/{movie_id}/similar'

        res = requests.get(URL, params=params)
        similar_items = res.json()['results']
        if len(similar_items) > 1:
            for i in range(len(similar_items)):
                similar_movies.append(similar_items[i])


    #유저가 좋아요한 recommended 영화 추천
    recommended_movies = []
    for movie_id in movie_ids_api:
        URL_2 = f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations'
        res_2 = requests.get(URL_2,params=params)
        recommended_itmes = res_2.json()['results']
        if len(recommended_itmes) > 1:
            for i in range(len(recommended_itmes)):
                recommended_movies.append(recommended_itmes[i])


    #유저가 좋아요한 장르별 영화 추천
    # user_genres = []
    # movie_genres = request.user.genre.all()
    # for i in movie_genres:
    #     user_genres.append(i.id)
    # recommend_movies_genre = Movie.objects.filter(genres__id = user_genres[0])
    # for i in user_genres[1:]:
    #     recommend_movies_genre = recommend_movies_genre|Movie.objects.filter(genres__id=i)
    # recommend_movies2 = recommend_movies_genre.order_by('-vote_average').distinct()[:10]
    
    # print('유사한영홧ㅂ',similar_movies)
    # print('fjsdlfjasdlkcjasdlcf',recommended_movies)
    context = {
        # 'form':form,
        'genres': genres,
        'movies': movies,
        'weekly_recommends1': weekly_recommends[:5],
        'weekly_recommends2': weekly_recommends[5:11],
        'similar_movies1':similar_movies[:5],
        'similar_movies2':similar_movies[5:11],
        'recommended_movies1':recommended_movies[:5],
        'recommended_movies2':recommended_movies[5:11],

        # 'recommend_movies_genre1': recommend_movies2[:5],
        # 'recommend_movies_genre2': recommend_movies2[5:10],
    }

    return render(request, 'movies/index.html', context)



#출연진 추가, 리뷰톡톡 추가..
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, movie_id=movie_pk)
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
        if len(similar_items)>1 and len(movie_credit)> 1:
            result = min(len(similar_items),len(movie_credit))
            for i in range(result):
                similar_movies.append(similar_items[i])
                actors.append(movie_credit[i])

        context = {
            'movie':movie,
            'similar_movies':similar_movies,
            'actors':actors,
        }
        return render(request,'movies/movie_detail.html',context)
    else:
        return redirect('accounts:login')




def movie_like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    print(user.pk,movie.movie_id,'hㅑㅋㅋ')
    if movie.like.filter(pk=user.pk).exists():
        movie.like.remove(user)
        liked=False
    else:
        movie.like.add(user)
        liked=True
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
    movie_name = request.GET.get('movie_name')
    search_movies = Movie.objects.filter(title__contains=movie_name)
    paginator = Paginator(search_movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(search_movies,'알ㄴ리ㅓ닝ㅊ')
    context = {
        'search_movies': search_movies,
        'page_obj': page_obj,
    }
    return render(request, 'movies/movie_list.html', context)





