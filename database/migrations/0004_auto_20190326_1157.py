# Generated by Django 2.1.7 on 2019-03-26 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20190325_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(),
        ),
    ]
