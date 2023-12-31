# Generated by Django 4.1.6 on 2023-03-09 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manger", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="resume",
            name="address",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="resume",
            name="agreeableness",
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name="resume",
            name="conscientiousness",
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name="resume",
            name="email",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="resume",
            name="extraversion",
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name="resume",
            name="fullname",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="resume",
            name="mobile",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="resume",
            name="neurotisum",
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name="resume",
            name="openess",
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name="resume",
            name="skills",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
