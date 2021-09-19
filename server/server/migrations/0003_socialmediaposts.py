# Generated by Django 3.2.7 on 2021-09-19 06:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20210919_0355'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaPosts',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=1000)),
                ('sentiment', models.DecimalField(decimal_places=3, max_digits=4)),
                ('magnitude', models.DecimalField(decimal_places=3, max_digits=5)),
                ('platform', models.CharField(max_length=250)),
                ('search_term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.searchterms')),
            ],
        ),
    ]
