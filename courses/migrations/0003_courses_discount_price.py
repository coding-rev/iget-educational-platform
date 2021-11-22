# Generated by Django 3.2.9 on 2021-11-20 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_episode_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=5),
            preserve_default=False,
        ),
    ]
