# Generated by Django 3.2.3 on 2021-06-17 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='units',
            new_name='dimension',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='name',
            new_name='title',
        ),
    ]