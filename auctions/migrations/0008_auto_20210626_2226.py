# Generated by Django 3.2.4 on 2021-06-26 17:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210626_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('1', 'Electronics'), ('2', 'Outdoors'), ('3', 'Handmade'), ('4', 'Sports'), ('5', 'Baby/Kids'), ('6', 'Tools')], default='6', max_length=1),
        ),
        migrations.AlterField(
            model_name='auction',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 26, 22, 26, 52, 142389)),
        ),
        migrations.AlterField(
            model_name='auction',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 26, 22, 26, 52, 142389)),
        ),
        migrations.AlterField(
            model_name='bid',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 26, 22, 26, 52, 144421)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 26, 22, 26, 52, 144421)),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 26, 22, 26, 52, 144421)),
        ),
    ]
