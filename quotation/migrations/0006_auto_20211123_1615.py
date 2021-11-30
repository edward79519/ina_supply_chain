# Generated by Django 3.2.9 on 2021-11-23 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0005_alter_itemquota_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemquota',
            name='crnt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='itemquota', to='quotation.current'),
        ),
        migrations.AlterField(
            model_name='itemquota',
            name='xchgrt',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=6, null=True),
        ),
    ]