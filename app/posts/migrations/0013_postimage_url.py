# Generated by Django 3.2 on 2022-04-14 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20220414_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='postimage',
            name='url',
            field=models.URLField(default='', max_length=500),
        ),
    ]
