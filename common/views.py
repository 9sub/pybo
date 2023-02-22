from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    if request.method == "POST": # post 요청이면 사용자 생성
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # 자동 로그인
            login(request, user) # 자동로그인
            return redirect('index')
    else: #get 요청이면 회원가입 페이지 보여주기
        form = UserForm()
    return render(request, 'common/signup.html', {'form':form})

