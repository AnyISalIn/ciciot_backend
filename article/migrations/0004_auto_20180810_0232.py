# Generated by Django 2.0.7 on 2018-08-10 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20180726_1757'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AddField(
            model_name='article',
            name='like',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='view',
            field=models.IntegerField(default=0),
        ),
    ]