# Generated by Django 3.1.3 on 2021-10-24 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0003_auto_20211024_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
