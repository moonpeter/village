# Generated by Django 3.2 on 2022-05-04 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionofthisweek',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='competitionofthisweek',
            name='closing_date',
            field=models.DateTimeField(null=True),
        ),
    ]
