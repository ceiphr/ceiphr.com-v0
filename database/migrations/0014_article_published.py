# Generated by Django 2.1.7 on 2019-04-15 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_auto_20190414_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
