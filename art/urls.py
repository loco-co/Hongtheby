from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('<int:item_id>/', views.detail),  # 매핑 룰에 의해 /art/item_id/가 적용되고 views.detail 함수가 실행됨
]
