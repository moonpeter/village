# Generated by Django 3.2 on 2022-04-06 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.TextField(default=''),
        ),
    ]
