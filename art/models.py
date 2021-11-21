from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_item')
    subject = models.CharField(max_length=200)
    title = models.CharField(max_length=20)
    price = models.IntegerField()
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    voter = models.ManyToManyField(User, related_name='voter_item')  # 추천인 추가

    def __str__(self):  # id 대신 제목을 반환하도록
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    voter = models.ManyToManyField(User, related_name='voter_comment')  # 추천인 추가
    reporter = models.ManyToManyField(User, related_name='reporter_comment')
