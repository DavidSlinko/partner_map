# Generated by Django 5.0.6 on 2024-06-05 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_map', '0010_alter_bonus_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonus',
            name='id_bonus',
            field=models.CharField(default=5674895068395638, max_length=200),
            preserve_default=False,
        ),
    ]
