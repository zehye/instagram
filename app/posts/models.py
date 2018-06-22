from django.conf import settings
from django.db import models

# posts앱의 class Post
#   author(settings.AUTH_USER_MODEL)
#   photo(ImageField)
#   content (Text)
#   created_at 를 작성하고 migrate
# ImageField를 위해서 Pillow 라이브러리 필요, 설치할 것
# pipenv install pillow


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # ImageField 는 파일필드를 상속받게 되어있다.
    # upload_to를 post를 했기 때문에 새로 생기는 폴더 이름도 post이다.
    photo = models.ImageField(upload_to='post', blank=True)

    # photo가 들어가면 굳이 content는 없어도 되니까 blank = True
    content = models.TextField(blank=True)

    # auth_now_add: 처음 만들어진 시간을 저장하고 auth_now: save가 될때마다 된다.
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f'작성자: {self.author}, ' \
    #            f'게시된 사진: {self.photo} - 게시글: {self.content}, ' \
    #            f'발행일자: {self.created_at}'
