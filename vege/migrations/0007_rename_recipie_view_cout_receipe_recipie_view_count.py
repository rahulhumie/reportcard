# Generated by Django 5.0.6 on 2024-06-19 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0006_alter_receipe_recipie_view_cout'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipe',
            old_name='recipie_view_cout',
            new_name='recipie_view_count',
        ),
    ]
