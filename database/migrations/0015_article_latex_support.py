# Generated by Django 2.1.7 on 2019-04-15 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0014_article_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='latex_support',
            field=models.BooleanField(default=False),
        ),
    ]
