from django.shortcuts import render, redirect, get_object_or_404
from .models import Genre, Movie, User_Vote, like_time
from .forms import User_VoteForm
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.paginator import Paginator
from accounts.forms import GenreChoiceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.views.decorators.http import require_POST

# Create your views here.
def genre_choice(request):
    user = request.user
    if request.method == 'POST':
        form = GenreChoiceForm(request.POST,instance=user)
        if form.is_valid():
            choice = form.save()
    return redirect('movies:index')

def index(request):
    if request.user.is_authenticated:
        form = GenreChoiceForm(instance=request.user)
    else:
        form = []
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    today = date.today()
    sevendays = today - timedelta(days=1)
    month_ago = today.replace(day=1) - timedelta(days=1)
    month_ago1 = month_ago.replace(day=1)
    movie_ids = like_time.objects.filter(created_at__range=[sevendays, today]).values('movie_id').annotate(movie_count=Count('movie_id')).order_by('-movie_count')[:10]
    movie_ids_month = like_time.objects.filter(created_at__range=[month_ago1, month_ago]).values('movie_id').annotate(movie_count=Count('movie_id')).order_by('-movie_count')[:10]

    recommend_movies = []
    recommend_movies_month = []
    for i in movie_ids:
        recommend_movies.append(Movie.objects.get(id=i['movie_id']))
    for j in movie_ids_month:
        recommend_movies_month.append(Movie.objects.get(id=j['movie_id']))

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
        'recommend_movies_days1': recommend_movies[:5],
        'recommend_movies_days2': recommend_movies[5:10],
        'recommend_movies_month1': recommend_movies_month[:5],
        'recommend_movies_month2': recommend_movies_month[5:10],
        'recommend_movies_genre1': recommend_movies2[:5],
        'recommend_movies_genre2': recommend_movies2[5:10],
    }
    return render(request, 'movies/index.html', context)

def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    form = User_VoteForm()
    User = get_user_model()
    evaluations = movie.user_vote_set.all()
    if movie.adult == 0:
        context = {
        'movie': movie,
        'form':form,
        'evaluations':evaluations,
        }

        return render(request, 'movies/movie_detail.html', context)
    else:
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            if user.is_adult != True:
                messages.warning(request, '미성년자는 볼수없습니다.')
                return redirect('movies:index')
            else:
                context = {
                'movie': movie,
                'form': form,
                'evaluations':evaluations,
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



# def movie_item(request):
#     API_KEY = ''
#     API_URL = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=ko-KR&sort_by=popularity.desc&include_adult=True&include_video=false&page='
#     for i in range(30,45):
#         response = requests.get(f'{API_URL}{i}')
#         jsonData = response.json()

#         for item in jsonData.get('results'):
#             movie = Movie()
#             movie.title = item.get('title')
#             movie.original_title = item.get('original_title')
#             movie.release_date = item.get('release_date')
#             movie.popularity = item.get('popularity')
#             movie.vote_count = item.get('vote_count')
#             movie.vote_average = item.get('vote_average')
#             movie.adult = item.get('adult')
#             movie.overview = item.get('overview')
#             movie.original_language = item.get('original_language')
#             movie.poster_path = item.get('poster_path')
#             movie.backdrop_path = item.get('backdrop_path')
#             movie.save()

#             for j in item.get('genre_ids'):
#                 genre = Genre.objects.get(id=j)
#                 movie.genres.add(genre)


#     return render(request, 'movies/test.html')

def movie_evaluate(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    if request.method == 'POST':
        form = User_VoteForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.user = request.user
            evaluation.movie = movie
            evaluation.save()
    return redirect('movies:movie_detail',movie_pk)

@login_required
def update_evaluate(request, evaluate_pk):
    evaluation = get_object_or_404(User_Vote, pk=evaluate_pk)
    if evaluation.user == request.user:
        if request.method == 'POST':
            form = User_VoteForm(request.POST, instance=evaluation)
            if form.is_valid():
                evaluation = form.save(commit=False)
                evaluation.user = request.user
                evaluation.save()
                return redirect('movies:movie_detail', evaluation.movie.pk)
        else:
            update_form = User_VoteForm(instance=evaluation)
            evaluations = evaluation.movie.user_vote_set.all()
            context = {
                'update_form':update_form,
                'movie': evaluation.movie,
                'evaluations':evaluations,
                'evaluate_pk':evaluate_pk,
            }
        return render(request,'movies/movie_detail.html', context)
    else:
        return redirect('movies:movie_detail', evaluation.movie.pk)

@login_required
@require_POST
def delete_evaluate(request,evaluate_pk):
    evaluation = get_object_or_404(User_Vote, pk=evaluate_pk)
    if request.user != evaluation.user:
        return redirect('movies:movie_detail', evaluation.movie.pk)
    else:
        evaluation.delete()
        return redirect('movies:movie_detail', evaluation.movie.pk)

# shift+alt+f 누르면 json 이쁘게나옴