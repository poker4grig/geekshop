# Generated by Django 3.2.7 on 2021-11-10 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_productcategory_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='discount',
            field=models.PositiveIntegerField(default=0, verbose_name='скидка'),
        ),
    ]
