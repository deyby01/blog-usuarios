# Generated by Django 5.2.2 on 2025-06-13 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_categoria_post_categoria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='categoria',
            new_name='categorias',
        ),
    ]
