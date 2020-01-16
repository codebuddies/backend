# Generated by Django 2.2.4 on 2020-01-08 06:14

from django.conf import settings
from django.db import migrations, models
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0003_auto_20190924_2157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='referrer',
            new_name='referring_url',
        ),
        migrations.RenameField(
            model_name='resource',
            old_name='credit',
            new_name='referring_user',
        ),
        migrations.AddField(
            model_name='resource',
            name='author',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='resource',
            name='user',
            field=models.ForeignKey(default=2, on_delete=models.SET(resources.models.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
    ]
