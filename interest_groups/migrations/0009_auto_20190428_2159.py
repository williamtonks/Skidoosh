# Generated by Django 2.1.5 on 2019-04-28 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interest_groups', '0008_auto_20190425_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussionpost',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='eventpost',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='/static/images/profile_pictures/default_profile_picture.jpg', upload_to='images/profile_pictures/'),
        ),
    ]