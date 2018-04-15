from django import forms

from .models import Post, Comment

# form to create new Blog Post
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

#Let your readers write comments
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)