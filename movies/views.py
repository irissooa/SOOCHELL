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


def home(request):
    return render(request,'movies/home.html')

# Create your views here.
# def genre_choice(request):
#     user = request.user
#     if request.method == 'POST':
#         form = GenreChoiceForm(request.POST,instance=user)
#         if form.is_valid():
#             choice = form.save()
#     return redirect('movies:index')


def index(request):
    if request.user.is_authenticated:
        form = GenreChoiceForm(instance=request.user)
    else:
        form = []
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    today = date.today()
    sevendays = today - timedelta(days=1)
    movie_ids = likeMovie.objects.filter(created_at__range=[sevendays,today]).values('movie_id').annotate(movie_count = Count('movie_id')).order_by('-movie_id')[::20]
    
    weekly_recommend = []
    for i in movie_ids:
        weekly_recommend.append(Movie.objects.get(id=i['movie_id']))

    recommend_movies2 = []
    if request.user.is_authenticated:
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
        'form':form,
        'genres': genres,
        'movies': movies,
        'recommend_movies_days1': weekly_recommend[:10],
        'recommend_movies_days2': weekly_recommend[5:10],
        'recommend_movies_genre1': recommend_movies2[:5],
        'recommend_movies_genre2': recommend_movies2[5:10],
    }
    return render(request, 'movies/index.html', context)



#출연진 추가, 리뷰톡톡 추가..
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    User = get_user_model()

    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        context = {
        'movie': movie,
        }
        return render(request, 'movies/movie_detail.html', context)
    else:
        return redirect('accounts:login')


def movie_like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.like.filter(pk=user.pk).exists():
        m1 = like_time.objects.filter(user=user).filter(movie=movie)
        m1.delete()
        liked = False
    else:
        m1 = like_time.objects.create(user=user,movie=movie)
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





