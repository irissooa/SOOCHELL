from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from movies.models import Genre
from .models import User

CHOICES = [(12,'action'),(14,'drama')]


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "사용자 아이디"})
    )
    is_adult = forms.BooleanField(
        label="성인입니까?",
        widget=forms.CheckboxInput(), required=False
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호(8자 이상)"})
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"})
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'is_adult', 'password1', 'password2']

class GenreChoiceForm(forms.ModelForm):

    genre = forms.ModelMultipleChoiceField(
            label='좋아하는 장르를 선택해주세요',
            queryset=Genre.objects.all(),
            widget=forms.CheckboxSelectMultiple(),
            required=False
            )


    class Meta:
        model = User
        fields = ['genre']
