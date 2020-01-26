# Generated by Django 2.2.9 on 2020-01-26 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("code_peg", "0002_auto_20200126_1120"),
    ]

    operations = [
        migrations.AlterField(
            model_name="codepeg",
            name="slot1",
            field=models.IntegerField(
                choices=[
                    (1, "Yellow"),
                    (2, "Blue"),
                    (3, "Purple"),
                    (4, "Orange"),
                    (5, "Green"),
                    (6, "Red"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="codepeg",
            name="slot2",
            field=models.IntegerField(
                choices=[
                    (1, "Yellow"),
                    (2, "Blue"),
                    (3, "Purple"),
                    (4, "Orange"),
                    (5, "Green"),
                    (6, "Red"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="codepeg",
            name="slot3",
            field=models.IntegerField(
                choices=[
                    (1, "Yellow"),
                    (2, "Blue"),
                    (3, "Purple"),
                    (4, "Orange"),
                    (5, "Green"),
                    (6, "Red"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="codepeg",
            name="slot4",
            field=models.IntegerField(
                choices=[
                    (1, "Yellow"),
                    (2, "Blue"),
                    (3, "Purple"),
                    (4, "Orange"),
                    (5, "Green"),
                    (6, "Red"),
                ]
            ),
        ),
    ]