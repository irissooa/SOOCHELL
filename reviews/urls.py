from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('',views.index,name='index'),
    path('create/',views.review_create, name='create_review'),
    path('<int:review_pk>/update/',views.update_review,name='update_review'),
    path('<int:review_pk>/delete/',views.delete_review,name='delete_review'),
    path('<int:review_pk>/',views.detail_review,name='detail_review'),
    path('<int:review_pk>/create/',views.create_comment,name='create_comment'),
    path('<int:review_pk>/<int:comment_pk>/update/',views.update_comment,name='update_comment'),
    path('<int:review_pk>/<int:comment_pk>/delete/',views.delete_comment,name='delete_comment'),
    path('<int:review_pk>/like/', views.like, name='like'),
]

