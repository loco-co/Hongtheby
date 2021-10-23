from django.shortcuts import render, get_object_or_404
from .models import Item

def index(request):
    """
    item 목록 출력
    """
    item_list = Item.objects.order_by('-create_date')
    context = {'item_list': item_list}
    return render(request, 'art/item_list.html', context)

def detail(request, item_id):  # 매개변수 id를 전달받음
    """
    item 내용 출력
    """
    item = get_object_or_404(Item, pk=item_id)  # 404에러 띄우기, 정상적이면 Item 객체에서 기본키로 객체를 찾아옴
    context = {'item': item}
    return render(request, 'art/item_detail.html', context)
