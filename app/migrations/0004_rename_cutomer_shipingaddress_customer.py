# Generated by Django 3.2.4 on 2021-07-26 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipingaddress',
            old_name='cutomer',
            new_name='customer',
        ),
    ]