from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm
from art.models import Item, Comment

def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def mypage(request):
    """
    마이페이지
    """
    my_item_list = Item.objects.order_by('-create_date')
    my_comment_list = Comment.objects.order_by('-create_date')
    context = {'my_item': my_item_list,
               'my_comment': my_comment_list, }
    return render(request, 'common/mypage.html', context)

def credit(request):
    """
    크레딧
    """
    return render(request, 'common/credit.html')
