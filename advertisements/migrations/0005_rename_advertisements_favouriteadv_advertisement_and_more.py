# Generated by Django 4.1.7 on 2023-03-08 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0004_alter_advertisement_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favouriteadv',
            old_name='advertisements',
            new_name='advertisement',
        ),
        migrations.RenameField(
            model_name='favouriteadv',
            old_name='users',
            new_name='user',
        ),
    ]
