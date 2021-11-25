from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Review, Comment
from movies.models import Movie
from .forms import ReviewForm, CommentForm
from django.http.response import JsonResponse
from django.http import HttpResponse

@login_required
@require_GET
def index(request):
    reviews = Review.objects.order_by('-pk')
    paginator = Paginator(reviews, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'reviews': reviews,
        'page_obj' : page_obj,
    }
    return render(request, 'community/index.html', context)





@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)

@login_required
@require_GET
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    # print(review.movie_title)
    movie = Movie.objects.filter(title = review.movie_title)
    poster = movie[0].poster_path
    movie_pk = movie[0].pk
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
        'poster': poster,
        'movie_pk': movie_pk,
    }
    return render(request, 'community/detail.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def update_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(instance=review)

        context = {'form': form,
                   'review': review,}
        return render(request, 'community/create.html', context)
    else:
        return redirect('community:detail', review.pk)


@login_required
@require_POST
def delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        review.delete()
    return redirect('community:index')


@login_required
@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('community:detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)

@login_required
@require_POST
def delete_comment(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('community:detail', review.pk)


@login_required
@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            liked = False
        else:
            review.like_users.add(user)
            liked = True
        like_status = {
            'liked' : liked,
            'count' : review.like_users.count()
        }
        # return redirect('community:index')
        return JsonResponse(like_status)
    # return redirect('accounts:login')
    return HttpResponse(status=401)

