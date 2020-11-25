from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm, GenreChoiceForm


# Create your views here.
def signup(request):
    # if request.user.is_authenticated:
    #     # 로그인되있으면 어디로 갈지 수정해야함
    #     return redirect('movies:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        form2 = GenreChoiceForm(request.POST)
        if form.is_valid() and form2.is_valid():
            user = form.save()
            form2.save()
            auth_login(request,user)
            # 어디로 갈지 수정해야함
            return redirect('movies:index')
    else:
        form=CustomUserCreationForm()
        form2 = GenreChoiceForm()
    context = {
        'form':form,
        'form2':form2,
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
    return redirect('movies:index')

