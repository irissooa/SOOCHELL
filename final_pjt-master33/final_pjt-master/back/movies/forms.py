from django import forms
from .models import User_Vote

class User_VoteForm(forms.ModelForm):
    content = forms.CharField(
        max_length=100,
        label='한줄평',
        widget=forms.TextInput(attrs={
            'placeholder': '한줄평을 작성해주세요',
            'size':70
        }))


    cnt = forms.IntegerField(
        required=True,
        label='평점',
        min_value=0,
        max_value=10,
        widget=forms.NumberInput()
        )
    class Meta:
        model = User_Vote
        fields = ['cnt','content']