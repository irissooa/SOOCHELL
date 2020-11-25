from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from movies.models import Genre
from .models import User
from movies.models import Genre



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={"placeholder":"ID"})
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder":"비밀번호(8자 이상)"})
    )
    password2 = forms.CharField(
        label="",
        widget = forms.PasswordInput(attrs={"placeholde":"비밀번호 확인"})
    )

    genre = forms.ModelMultipleChoiceField(
        label='좋아하는 장르를 선택해주세요',
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','password1','password2','genre']


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
