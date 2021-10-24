from django.db import models


class Item(models.Model):
    subject = models.CharField(max_length=200)
    title = models.CharField(max_length=20)
    price = models.IntegerField()
    content = models.TextField()
    create_date = models.DateTimeField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):  # id 대신 제목을 반환하도록
        return self.title
