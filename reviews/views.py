from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from django.core.paginator import Paginator
from .models import Review, Comment
from .forms import ReviewForm, CommentForm

# Create your views here.

def index(request):
    reviews = Review.objects.order_by('-pk')
    paginator = Paginator(reviews,20)
    page_number = request.GET.get('page')
    per_page = paginator.get_page(page_number)
    context = {
        'reviews':reviews,
        'per_page':per_page,
    }
    #페이지 다시
    return render(request,'reviews/index.html',context)


@login_required
def create_review(request):
    if request.method == 'POST':
        form  = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            #페이지 다시
            return redirect('reviews:review_detail',review.pk)

    else:
        form=ReviewForm()
    context = {
        'form':form,
    }
    return render(request,'reviews/form.html',context)



@login_required
def detail_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm()
    comments = review.comment_set.all()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'reviews/review_detail.html', context)



@login_required
def update_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:detail_review', review.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form,
    }
    return render(request, 'reviews/form.html', context)



@login_required
@require_POST
def delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user != review.user:
        return redirect('reviews:detail_review', review.pk)
    else:
        review.delete()
        return redirect('reviews:index')
    

@login_required
@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
    return redirect('reviews:detail_review', review_pk)


@login_required
def update_comment(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    review = get_object_or_404(Review, pk=review_pk)
    if comment.user == request.user:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.review = review
                comment.save()
                return redirect('reviews:detail_review', comment.review.pk)
        else:
            update_form = CommentForm(instance = comment)
            comments = review.comment_set.all()
            context = {
                'update_form':update_form,
                'review':review,
                'comments':comments,
                'comment_pk':comment_pk
            }
        return render(request,'reviews/review_detail.html', context)
    else:
        return redirect('reviews:detail_review', comment.review.pk)
    


@login_required
@require_POST
def delete_comment(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('reviews:detail_review', review_pk)



@require_POST
def like(request, review_pk):
    context = {
        'error' : 'unauthorized'
    }
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            liked = False
        else:
            review.like_users.add(user)
            liked = True
        context = {
            'liked' : liked,
            'count' : review.like_users.count(),
        }
    return JsonResponse(context)
