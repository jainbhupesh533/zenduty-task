# Generated by Django 5.0.1 on 2024-01-22 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_rename_name_books_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(db_index=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='books',
            name='title',
            field=models.CharField(db_index=True, max_length=150),
        ),
    ]
