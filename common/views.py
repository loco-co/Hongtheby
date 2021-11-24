from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm
from art.models import Item, Comment
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

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

@login_required(login_url='common:login')
def mypage(request):
    """
    마이페이지
    """
    my_item_list = Item.objects.order_by('-create_date')
    my_item_list = my_item_list.filter(
        Q(author__username__icontains=request.user)
    )
    my_comment_list = Comment.objects.order_by('-create_date')
    my_comment_list = my_comment_list.filter(
        Q(author__username__icontains=request.user)
    )
    context = {'my_item': my_item_list,
               'my_comment': my_comment_list, }
    return render(request, 'common/mypage.html', context)

def credit(request):
    """
    크레딧
    """
    return render(request, 'common/credit.html')

@login_required(login_url='common:login')
def my_item(request):
    """
    내가 쓴 글 전체
    """
    my_item_list = Item.objects.order_by('-create_date')
    my_item_list = my_item_list.filter(
        Q(author__username__icontains=request.user)
    )
    page = request.GET.get('page', '1')
    paginator = Paginator(my_item_list, 6)  # 페이지당 6개씩 보여주기
    page_obj = paginator.get_page(page)  # 1페이지의 페이징 객체 생성, 전체를 조회하지 않음

    context = {'my_item_list': page_obj, 'page': page}

    return render(request, 'common/my_item.html', context)

@login_required(login_url='common:login')
def my_comment(request):
    """
    내가 쓴 댓글 전체
    """
    my_comment_list = Comment.objects.order_by('-create_date')
    my_comment_list = my_comment_list.filter(
        Q(author__username__icontains=request.user)
    )

    context = {'my_comment': my_comment_list}
    return render(request, 'common/my_comment.html', context)
