# Generated by Django 2.0.7 on 2018-07-26 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20180726_0824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['pub_date']},
        ),
        migrations.RenameField(
            model_name='article',
            old_name='category',
            new_name='categorise',
        ),
    ]
