# Generated by Django 3.2 on 2022-04-07 07:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('ct001', '일상'), ('ct002', '고민상담'), ('ct003', '연애'), ('ct004', '질문'), ('ct005', '여가'), ('ct006', '취향'), ('ct007', '재테크'), ('ct008', '다이어트'), ('ct009', '취미생활')], default='test', max_length=20),
        ),
        migrations.AddField(
            model_name='post',
            name='mbti_tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('INTJ', 'INTJ'), ('INTP', 'INTP'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'), ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'), ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'), ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP')], max_length=4), default=['INTJ'], size=None),
        ),
    ]
