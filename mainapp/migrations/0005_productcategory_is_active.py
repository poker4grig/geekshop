# Generated by Django 3.2.7 on 2021-11-09 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_product_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
