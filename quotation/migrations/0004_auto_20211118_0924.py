# Generated by Django 3.2.9 on 2021-11-18 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0003_auto_20211117_1511'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='is_valid',
            new_name='is_open',
        ),
        migrations.RenameField(
            model_name='inquiry',
            old_name='is_valid',
            new_name='is_open',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='is_valid',
            new_name='is_open',
        ),
        migrations.RenameField(
            model_name='itemquota',
            old_name='is_valid',
            new_name='is_open',
        ),
    ]
