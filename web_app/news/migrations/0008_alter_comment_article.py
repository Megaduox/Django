# Generated by Django 3.2 on 2021-06-22 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20210527_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.article'),
        ),
    ]
