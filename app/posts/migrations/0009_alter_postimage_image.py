# Generated by Django 3.2 on 2022-04-14 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_postimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.ImageField(null=True, upload_to='posts/images'),
        ),
    ]
