# Generated by Django 3.1.3 on 2020-12-12 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_auto_20201212_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='product',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]