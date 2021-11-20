from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['title', 'movie_title', 'rank', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'글의 제목을 작성하세요'}),
            'movie_title': forms.TextInput(attrs={'placeholder':'영화명을 작성하세요'}),
            # 'rank': forms.Select(attrs={'placeholder':'평점을 선택하세요'}),
            'content': forms.Textarea(attrs={'placeholder':'리뷰를 작성하세요'}),
        }
        labels = {
            'title' : '글 제목',
            'movie_title' : '영화명',
            'rank': '평점',
            'content':'리뷰작성',
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['review', 'user']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder':'댓글을 작성하세요', 'rows':1,})
        }
        labels = {
            'content':'댓글',
        }
