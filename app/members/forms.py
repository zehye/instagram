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
    gender = forms.CharField(
        label='성별',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
            choices=User.CHOICES_GENDER,
        )
    )

    img_profile = forms.FileField(
        label='프로필 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )

    introduce = forms.CharField(
        label='소개',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )

    site = forms.URLField(
        label='사이트 URL',
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
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
        fields = [
            'username',
            'email',
            'password',
            'gender',
            'site',
            'img_profile',
            'introduce',
        ]
        # create_user_dict = {
        #     'username': self.cleaned_data['username'],
        #     'email': self.cleaned_data['email'],
        #     'password': self.cleaned_data['password'],
        #     'gender': self.cleaned_data['gender'],
        #     'site': self.cleaned_data['site'],
        #     'img_profile': self.cleaned_data['img_profile'],
        #     'introduce': self.cleaned_data['introduce'],
        #
        # }
        #
        create_user_dict = {}
        for key, value in self.cleaned_data.items():
            if key in fields:
                create_user_dict[key] = value

        # dict comprehension 사용
        # create_user_dict = {key: value for (key, value) in self.cleaned_data.items() if key in fields}

        # filter 사용
        # def in_fields(item):
        #     return item[0] in fields
        #
        # self.cleaned_date.items() = (('username', 'pjh'), ('passworld','pjh~'))
        # result = filter(in_fields, self.cleaned_data.items())
        # create_user = {}
        # for item in result:
        #     create_user_dict[item[0]] = item[1]
        #
        # create_user_dict = dict(filter(in_fields, self.cleaned_date.items()))
        # create_user_dict_lambda = dict(filter(lambda item: item[0] in fields, self.cleaned_date.items()))

        user = User.objects.create_user(**create_user_dict)
        # username = self.cleaned_data['username']
        # email = self.cleaned_data['email']
        # password = self.cleaned_data['password']
        # gender = self.cleaned_data['gender']
        # img_profile = self.cleaned_data['img_profile']
        # site = self.cleaned_data['site']
        # introduce = self.cleaned_data['introduce']
        #
        # user = User.objects.create_user(
        #     username=username,
        #     password=password,
        #     email=email,
        #     gender=gender,
        #     img_profile=img_profile,
        #     site=site,
        #     introduse=introduce,
        # )

        return user

