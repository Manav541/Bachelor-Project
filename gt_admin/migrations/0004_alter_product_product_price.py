# Generated by Django 3.2.9 on 2022-03-13 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gt_admin', '0003_alter_product_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.IntegerField(),
        ),
    ]