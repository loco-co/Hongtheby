from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    title = models.CharField(max_length=20)
    price = models.IntegerField()
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):  # id 대신 제목을 반환하도록
        return self.title
