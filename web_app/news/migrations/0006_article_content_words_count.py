# Generated by Django 3.2 on 2021-05-18 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content_words_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
