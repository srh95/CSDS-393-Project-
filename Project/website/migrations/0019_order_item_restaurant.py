# Generated by Django 3.2 on 2021-05-06 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='item_restaurant',
            field=models.IntegerField(default=0),
        ),
    ]
