# Generated by Django 3.2.9 on 2022-01-14 10:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0017_del_field_subspec_is_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='addtime',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 1, 14, 10, 14, 59, 914547, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='category',
            name='updatetime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='historicalcategory',
            name='addtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 14, 10, 15, 27, 886370, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalcategory',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='historicalcategory',
            name='updatetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 14, 10, 15, 36, 326205, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
    ]
