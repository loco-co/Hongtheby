from django.urls import path
from . import views


app_name = 'art'

urlpatterns = [
    path('', views.index, name='index'),  # url별칭 사용
    path('<int:item_id>/', views.detail, name='detail'),  # 매핑 룰에 의해 /art/item_id/가 적용되고 views.detail 함수가 실행됨
    path('item/create/', views.item_create, name='item_create'),
    path('item/modify/<int:item_id>/', views.item_modify, name='item_modify'),
    path('item/delete/<int:item_id>/', views.item_delete, name='item_delete'),
]
