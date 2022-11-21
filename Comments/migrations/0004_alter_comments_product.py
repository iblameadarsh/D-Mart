# Generated by Django 3.2.15 on 2022-09-26 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BuyNow', '0008_product_user'),
        ('Comments', '0003_auto_20220907_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='BuyNow.product'),
        ),
    ]