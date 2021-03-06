# Generated by Django 3.2.4 on 2021-06-24 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_bid_comment_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='closePrice',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='duration',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='image',
            field=models.URLField(default='https://static.umotive.com/img/product_image_thumbnail_placeholder.png'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='lastBid',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='win',
            field=models.BooleanField(default=False),
        ),
    ]
