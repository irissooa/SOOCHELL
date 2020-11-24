from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie_list/<int:genre_id>/', views.movie_list, name='movie_list'),
    path('movie_detail/<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/like/', views.movie_like, name="movie_like"),
    path('<int:movie_pk>/evaluate/', views.movie_evaluate, name="movie_evaluate"),
    path('search/', views.movie_search, name="movie_search"),
    path('genre_choice/', views.genre_choice, name='genre_choice'),
    path('<int:evaluate_pk>/delete/', views.delete_evaluate, name='delete_evaluate'),
    path('<int:evaluate_pk>/update/', views.update_evaluate, name='update_evaluate'),
]
