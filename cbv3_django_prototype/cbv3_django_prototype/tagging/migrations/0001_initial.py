# Generated by Django 2.2.4 on 2020-02-29 23:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(default=uuid.uuid1, editable=False)),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'db_table': 'tagging_custom_tag',
            },
        ),
    ]
