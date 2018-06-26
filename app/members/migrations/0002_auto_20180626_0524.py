# Generated by Django 2.0.6 on 2018-06-26 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', '남성'), ('F', '여성'), ('x', '선택안함')], default='x', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='img_profile',
            field=models.ImageField(blank=True, upload_to='user'),
        ),
        migrations.AddField(
            model_name='user',
            name='introduce',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='site',
            field=models.URLField(blank=True),
        ),
    ]
