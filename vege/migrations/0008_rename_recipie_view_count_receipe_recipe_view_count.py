# Generated by Django 5.0.6 on 2024-06-19 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0007_rename_recipie_view_cout_receipe_recipie_view_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipe',
            old_name='recipie_view_count',
            new_name='recipe_view_count',
        ),
    ]
