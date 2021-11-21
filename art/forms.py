from django import forms
from art.models import Item, Comment


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item  # 사용할 모델
        fields = ['subject', 'title', 'price', 'content', 'image', 'category']
        labels = {
            'subject': '글제목',
            'title': '작품명',
            'content': '내용',
            'price': '가격',
            'image': '사진 업로드',
            'category': '종류'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }
