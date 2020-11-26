from django import forms
from .models import Comment, Review



class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['title','content',]



class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=100,
    label="",
    widget=forms.TextInput(attrs={'placeholder': 'Share your idea!','size':100}))
    class Meta:
        model = Comment
        fields = ['content']
