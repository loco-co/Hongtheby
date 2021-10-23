from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['subject']  # 제목으로 검색하는 관리자 기능 추가

admin.site.register(Item)  # 관리자 사이트에 모델 등록
