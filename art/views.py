from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Comment
from .forms import ItemForm, CommentForm
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

def index(request):
    """
    item 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # get 방식으로 호출된 페이지 중 1페이지, 디폴트는 1
    kw = request.GET.get('kw', '')  # 검색어

    # 작성순으로 조회
    item_list = Item.objects.order_by('-create_date')
    if kw:
        item_list = item_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw)  # 질문 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(item_list, 6)  # 페이지당 6개씩 보여주기
    page_obj = paginator.get_page(page)  # 1페이지의 페이징 객체 생성, 전체를 조회하지 않음

    context = {'item_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'art/item_list.html', context)

def detail(request, item_id):  # 매개변수 id를 전달받음
    """
    item 내용 출력
    """
    item = get_object_or_404(Item, pk=item_id)  # 404에러 띄우기, 정상적이면 Item 객체에서 기본키로 객체를 찾아옴
    context = {'item': item}
    return render(request, 'art/item_detail.html', context)

@login_required(login_url='common:login')
def item_create(request):
    """
    item 게시글 등록
    """
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        date = timezone.now()
        price = request.POST['price']
        subject = request.POST['subject']
        img = request.FILES['image']
        user = request.user
        item = Item(
            title=title,
            content=content,
            create_date=date,
            price=price,
            subject=subject,
            image=img,
            author=user,
        )
        item.save()
        return redirect('art:index')
    else:
        form = ItemForm()
    context = {'form': form}  # 템플릿에서 글등록시 사용할 폼 엘리먼트를 위해
    return render(request, 'art/item_form.html', context)

@login_required(login_url='common:login')
def item_modify(request, item_id):
    """
    item 게시글 수정
    """
    item = get_object_or_404(Item, pk=item_id)
    if request.user != item.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('art:detail', item_id=item.id)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.modify_date = timezone.now()  # 수정일시 저장
            item.save()
            return redirect('art:detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
    context = {'form': form}
    return render(request, 'art/item_form.html', context)

@login_required(login_url='common:login')
def item_delete(request, item_id):
    """
    item 게시글 삭제
    """
    item = get_object_or_404(Item, pk=item_id)
    if request.user != item.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('art:detail', item_id=item.id)
    item.delete()
    return redirect('art:index')

@login_required(login_url='common:login')
def comment_create(request, item_id):
    """
    item 댓글 등록
    """
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.item = item
            comment.save()
            return redirect('art:detail', item_id=item.id)
    else:
        return redirect('art:detail', item_id=item.id)

@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    """
    item 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('art:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('art:detail', item_id=comment.item.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'art/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    """
    item 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('art:detail', item_id=comment.item.id)
    else:
        comment.delete()
    return redirect('art:detail', item_id=comment.item.id)

def vote_item(request, item_id):
    """
    item 추천
    """
    item = get_object_or_404(Item, pk=item_id)
    if request.user == item.author:
        messages.warning(request, '본인이 작성한 글은 추천할수 없습니다')
    if request.user in item.voter.all():
        messages.warning(request, '이미 추천한 게시글입니다')
    else:
        item.voter.add(request.user)
    return redirect('art:detail', item_id=item.id)
