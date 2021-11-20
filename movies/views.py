from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from .models import Movie, Genre_movie
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
from itertools import chain


# Create your views here.
@require_safe
def index(request):
    movies = Genre_movie.objects.order_by("?")
    
    paginator = Paginator(movies, 15)

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


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # genres = movie.genres.filter(movie=movie_pk)
    genres = movie.genres.filter()
    # print(genres)
    context = {
        'movie' : movie,
        'genres' : genres,
    }
    return render(request, 'movies/detail.html', context)

@require_safe
def detail2(request, genre_movie_pk):
    movie = get_object_or_404(Genre_movie, pk=genre_movie_pk)
    genres = movie.genres.filter()
    # print(genres)
    context = {
        'movie' : movie,
        'genres' : genres,
    }
    return render(request, 'movies/detail2.html', context)    


@require_safe
def recommended(request):
    movies = Movie.objects.order_by('-vote_average')[:10]

    context = {
        'movies' : movies
    }    
    return render(request, 'movies/recommended.html', context)

@require_safe
def random(request):
    movies = Movie.objects.all()
    # movie_list = {}
    # for i in range(len(movies)):
    #     movie_list[str(i)] = movies[i].title
    # print(movie_list)
    # data = serializers.serialize('json', )
    movie_list = []

    # /movies/?page=2 ajax 요청 => json
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        for i in range(len(movies)):
            movie_dict = {}
            movie = movies[i]
            movie_dict['randommovie_pk'] = movie.pk 
            movie_dict['title'] = movie.title
            movie_dict['overview'] = movie.overview
            movie_list.append(movie_dict)
        return JsonResponse(movie_list, safe=False)
    else:
        return render(request, 'movies/random.html')
    # /movies/ 첫번째 페이지 요청 => html

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
    


def genre_recommend(request, genre_movie_pk):
    movie = get_object_or_404(Genre_movie, pk=genre_movie_pk)
    selectedgenres = movie.genres.all()
    # print(selectedgenres[0].name)
    movies = Genre_movie.objects.filter(genres=selectedgenres[0])
    # movies = list(movies)
    print(Genre_movie.objects.filter(genres=selectedgenres[0]))
    second_movies = Movie.objects.filter(genres=selectedgenres[0])
    # second_movies = list(second_movies)
    results = Genre_movie.objects.filter(genres=selectedgenres[0]).values("title", "poster_path").union(Movie.objects.filter(genres=selectedgenres[0]).values("title", "poster_path"))
    print(results)

    # for b in second_movies:
    #     if b not in movies:
    #         movies.append(b)
                  
    context = {
        'movie': movie,
        'selectedgenres': selectedgenres,
        'movies': movies,
        'second_movies': second_movies,
        'results': results,
      
      
    }
    return render(request, 'movies/genre_recommend.html', context)
    
