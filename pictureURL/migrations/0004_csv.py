# Generated by Django 2.2.7 on 2020-03-03 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictureURL', '0003_auto_20200228_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auid', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=100)),
                ('csv_path', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
