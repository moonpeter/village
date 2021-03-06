# Generated by Django 3.2 on 2022-04-20 08:21

import common.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_alter_pollquestion_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='image',
            field=models.ImageField(upload_to=common.utils.rename_imagefile_to_uuid_for_comment),
        ),
        migrations.AlterField(
            model_name='postsubcomment',
            name='image',
            field=models.ImageField(upload_to=common.utils.rename_imagefile_to_uuid_for_comment),
        ),
    ]
