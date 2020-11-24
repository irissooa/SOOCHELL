from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('',views.index,name='index'),
    path('create/',views.create_article,name='create_article'),
    path('<int:article_pk>/update/',views.update_article,name='update_article'),
    path('<int:article_pk>/delete/',views.delete_article,name='delete_article'),
    path('<int:article_pk>/',views.detail_article,name='detail_article'),
    path('<int:article_pk>/create/',views.create_comment,name='create_comment'),
    path('<int:article_pk>/<int:comment_pk>/update/',views.update_comment,name='update_comment'),
    path('<int:article_pk>/<int:comment_pk>/delete/',views.delete_comment,name='delete_comment'),
]