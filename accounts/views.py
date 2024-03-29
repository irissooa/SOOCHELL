from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, GenreChoiceForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
# from .forms import CustomUserCreationForm
import requests


# Create your views here.
def signup(request):
    # if request.user.is_authenticated:
    #     # 로그인되있으면 어디로 갈지 수정해야함
    #     return redirect('movies:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('movies:movie_select')
    else:
        form=CustomUserCreationForm()
    
    #오늘의 트렌딩 영화
    API_KEY='48bad6a2dc7df8164930b0ed851e6d37'
    URL = 'https://api.themoviedb.org/3/trending/movie/day'
    params = {'api_key':API_KEY}

    res = requests.get(URL,params=params)

    trending_itmes = res.json()['results']
    context = {
        'form':form,
        'trending_items1':trending_itmes[:6],
        'trending_items2':trending_itmes[6:12],
    }
    return render(request,'accounts/signup.html',context)


def login(request):
    if request.user.is_authenticated:
        # 어디로 갈지 수정해야함
        return redirect('movies:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())
            # 어디로 갈지 수정해야함
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form=AuthenticationForm()
    context={
        'form':form,
    }
    return render(request,'accounts/login.html',context)


@login_required
def logout(request):
    auth_logout(request)
     # 어디로 갈지 수정해야함
    return redirect('accounts:signup')

