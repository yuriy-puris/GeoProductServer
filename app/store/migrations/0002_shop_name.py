# Generated by Django 2.2.7 on 2019-11-25 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='name',
            field=models.CharField(default='name', max_length=50),
        ),
    ]
