from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from .models import Movie, Genre_movie
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse


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
    genres = movie.genres.filter(movie=movie_pk)
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
    print(genres)
    context = {
        'movie' : movie,
        'genres' : genres,
    }
    return render(request, 'movies/detail2.html', context)    


@require_safe
def recommended(request):
    movies = Movie.objects.order_by('vote_average')[:10]

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
