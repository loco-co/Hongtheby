from django.shortcuts import render, get_object_or_404
from .models import Item
from django.core.paginator import Paginator


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
