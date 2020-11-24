from django import forms
from .models import Comment, Review


CHOICES = [("Good"),("So SO"),("Bad")]

class ReviewForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Review
        fields = ['title','content','category',]



class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=100,
    label="",
    widget=forms.TextInput(attrs={'placeholder': 'Share your idea!','size':100}))
    class Meta:
        model = Comment
        fields = ['content']
