from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:genre_movie_pk>/genre_movie', views.detail2, name='detail2'),
    path('recommended/', views.recommended, name='recommended'),
]
