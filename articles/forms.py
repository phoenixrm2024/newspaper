# articles/forms.py

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'author')

# ModelForm; a helper class designed to translate database models into forms.