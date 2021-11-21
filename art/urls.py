from django.urls import path
from . import views


app_name = 'art'

urlpatterns = [
    path('', views.index, name='index'),  # url별칭 사용
    path('<int:item_id>/', views.detail, name='detail'),  # 매핑 룰에 의해 /art/item_id/가 적용되고 views.detail 함수가 실행됨
    path('item/create/', views.item_create, name='item_create'),
    path('item/modify/<int:item_id>/', views.item_modify, name='item_modify'),
    path('item/delete/<int:item_id>/', views.item_delete, name='item_delete'),
    path('comment/create/item/<int:item_id>/', views.comment_create, name='comment_create'),
    path('comment/modify/item/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('comment/delete/item/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('vote/item/<int:item_id>/', views.vote_item, name='vote_item'),
    path('vote/comment/<int:comment_id>/', views.vote_comment, name='vote_comment'),
    path('report/comment/<int:comment_id>/', views.report_comment, name='report_comment'),
    path('sculpture/', views.sculpture_view, name='sculpture_view'),
    path('ceramic/', views.ceramic_view, name='ceramic_view'),
]
