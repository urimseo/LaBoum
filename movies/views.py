from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_safe
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre_movie
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
from itertools import chain

import requests
from Laboum import settings
from .forms import MovieSearchForm

from django.db.models import Q
# 검색기능 

def search(request):
    movies = Movie.objects.all()
    genre_movies = Genre_movie.objects.all()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            movies = movies.filter(Q(title__icontains=keyword)| Q(title__istartswith=keyword[:2]))
            genre_movies = genre_movies.filter(Q(title__icontains=keyword)| Q(title__istartswith=keyword[:2]))
            if movies:
                movie_pk = movies[0].pk

                return redirect('movies:detail', movie_pk)

            # movies = genre_movies.filter(Q(title__icontains=keyword)| Q(title__istartswith=keyword[:2]))
            elif genre_movies:
                movie_pk = genre_movies[0].pk
                return redirect('movies:detail2', movie_pk)

    # context = {
    #     'err' : '검색 결과가 없습니다.'
    # }
    return redirect('movies:index')     



# Create your views here.
@login_required
@require_safe
def index(request):
    movies = Genre_movie.objects.order_by("?")
    
    paginator = Paginator(movies, 36)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # /movies/?page=2 ajax 요청 => json
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = serializers.serialize('json', page_obj)
        return HttpResponse(data, content_type='application/json')
    # /movies/ 첫번째 페이지 요청 => html
    else:
        context = {
            'movies': page_obj,
        }

        return render(request, 'movies/index.html', context)

@login_required
@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # genres = movie.genres.filter(movie=movie_pk)
    genres = movie.genres.filter()
    # print(genres)

    ## youtube api로 예고편 가져오기
    # print(movie)
    keyword = f'영화 {movie} 예고편'
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': settings.YOUTUBE_API_KEY,
        'part': 'snippet',
        'type': 'video',
        'maxResults': '1',
        'q': keyword,
    }
    response = requests.get(url, params)
    response_dict = response.json()
    videoId = response_dict['items'][0]['id']['videoId']

    context = {
        'movie' : movie,
        'genres' : genres,
        'videoId' : videoId,
        'youtube_items': response_dict['items']
    }
    return render(request, 'movies/detail.html', context)

@login_required
@require_safe
def detail2(request, genre_movie_pk):
    movie = get_object_or_404(Genre_movie, pk=genre_movie_pk)
    genres = movie.genres.filter()

    # youtube api
    # print(movie)
    keyword = f'영화 {movie} 예고편'
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': settings.YOUTUBE_API_KEY,
        'part': 'snippet',
        'type': 'video',
        'maxResults': '1',
        'q': keyword,
    }
    response = requests.get(url, params)
    response_dict = response.json()
    videoId = response_dict['items'][0]['id']['videoId']
    context = {
        'movie' : movie,
        'genres' : genres,
        # youtube
        'videoId' : videoId,
        'youtube_items': response_dict['items']
    }
    return render(request, 'movies/detail2.html', context)    

@login_required
@require_safe
def recommended(request):
    movies = Genre_movie.objects.order_by('-grade')[:10]

    context = {
        'movies' : movies
    }    
    return render(request, 'movies/recommended.html', context)

@login_required
def color(request):
    reds = Movie.objects.filter(genres__in=[80, 10752,28, 37])
    yellows = Movie.objects.filter(genres__in=[35, 18])
    pinks = Movie.objects.filter(genres__in=[10749, 16])
    greens = Movie.objects.filter(genres__in=[10751, 99, 10402])
    blues = Movie.objects.filter(genres__in=[878, 14])
    purples = Movie.objects.filter(genres__in=[9648, 53, 27])
    context = {}
    if 'keyword' in request.POST:
        if 'red' == request.POST.get('keyword'):
            context = {
                'reds' : reds
            }
        elif 'yellow' == request.POST.get('keyword'):
            context = {
                'yellows' : yellows
            }
        elif 'pink' == request.POST.get('keyword'):
            context = {
                'pinks' : pinks
            }
        elif 'green' == request.POST.get('keyword'):
            context = {
                'greens' : greens
            }
        elif 'blue' == request.POST.get('keyword'):
            context = {
                'blues' : blues
            }
        elif 'purple' == request.POST.get('keyword'):
            context = {
                'purples' : purples
            }
    return render(request, 'movies/color.html', context)
    

@login_required
def genre_recommend(request, genre_movie_pk):
    movie = get_object_or_404(Genre_movie, pk=genre_movie_pk)
    selectedgenres = movie.genres.all()
    movies = Genre_movie.objects.filter(genres=selectedgenres[0])
    # print(Genre_movie.objects.filter(genres=selectedgenres[0]))
    second_movies = Movie.objects.filter(genres=selectedgenres[0])


                  
    context = {
        'movie': movie,
        'selectedgenres': selectedgenres,
        'movies': movies,
        'second_movies': second_movies,

    }
    return render(request, 'movies/genre_recommend.html', context)
    
