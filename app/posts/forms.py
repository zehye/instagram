from django import forms

from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    # field정의를 직접하지 않음
    # 어떤 field를 사용할 것인지만 class Meta에 기록
    class Meta:
        model = Post
        fields = ['photo', 'content']


class PostForm(forms.Form):
    photo = forms.ImageField(
        label='사진',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def save(self, author):
        return Post.objects.create(
            author=author,
            photo=self.cleaned_data['photo'],
            content=self.cleaned_data['content'],
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
