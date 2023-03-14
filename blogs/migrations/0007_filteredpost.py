# Generated by Django 3.2 on 2023-03-14 06:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilteredPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('excerpt', models.CharField(max_length=200)),
                ('image', models.ImageField(null=True, upload_to='posts')),
                ('date', models.DateField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField(validators=[django.core.validators.MinLengthValidator(10)])),
                ('view_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='filtered_posts', to='blogs.author')),
                ('tags', models.ManyToManyField(to='blogs.Tag')),
            ],
        ),
    ]