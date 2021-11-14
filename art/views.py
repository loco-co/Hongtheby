from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from .forms import ItemForm
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    """
    item 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # get 방식으로 호출된 페이지, 디폴트는 1

    # 작성순으로 조회
    item_list = Item.objects.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(item_list, 8)  # 페이지당 8개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'item_list': page_obj}
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
