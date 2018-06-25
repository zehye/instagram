from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib.auth.views import login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# User클래스 자체를 가져올때는 get_user_model()
# ForeignKey에 User모델을 지정할 때는 settings.AUTH_USER_MODEL
User = get_user_model()


def login_view(request):
    # print(request.POST)
    # 인증에 성공하면 posts:post-list로 이동
    # 실패하면 다시 members:login으로 이동

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # 인증에 성공한 경우
        if user is not None:
            # 세션값을 만들어 DB에 저장하고, HTTP response의 Cookie에 해당값을 담아보내도록 하는
            # login()함수를 실행한다.
            login(request, user)
            return redirect('posts:post-list')
        # 인증에 실패한 경우(username, password가 틀린경우
        else:
            # 다시 로그인 페이지로 이동
            return redirect('members:login')
    else:
        return render(request, 'members/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


def signup(request):
    context = {
        'errors': [],
    }

    if request.method == 'POST':
        # exists를 사용해서 유저가 이미 존재하면 signup으로 다시 redirect
        # 존재하지 않는 경우에만 아래 조직 실행
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # 두번째 검사로, password와 password2가 같은지 검사
        # 다를 경우, 해당 오류를 출력
        # username도 이미 존재하고 password도 다를 경우, 둘다 출력
        password2 = request.POST['password2']

        context['username'] = username
        context['email'] = email

        # form에서 전송된 데이터들이 올바른지 검사
        if User.objects.filter(username=username).exists():
            context['errors'].append('유저가 이미 존재함')

        if password != password2:
            context['errors'].append('패스워드가 일치하지 않음')

        # errors가 없으면 유저 생성 루틴 실행
        if not context['errors']:
            # errors가 없으면 유저 생성 루틴 실행
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            login(request, user)
            return redirect('index')

    return render(request, 'members/signup.html', context)
