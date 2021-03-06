# Generated by Django 3.2.3 on 2021-06-23 11:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0007_purchase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='shopper',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='purchase',
            unique_together={('user', 'recipe')},
        ),
    ]
