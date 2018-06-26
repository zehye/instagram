from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.Form):
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        label='이메일',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    def clean_username(self):
        # username field의 clean()실행 결과가 self.cleaned_data['username']에 있음
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('아이디가 이미 존재합니다.')
        return username

    def clean(self):
        # cleaned_data를 데려올때 사용하는 방법
        # clean이 반드시 cleaned_data를 가져오는 것에 대해 제약이 없다.

        # 상위 클래스가 어떻게 되어있냐에 따라 다르다.
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password2 != password:
            # raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
            self.add_error('password2', '비밀번호가 일치하지 않습니다.')
        return self.cleaned_data

    def signup(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        return user
