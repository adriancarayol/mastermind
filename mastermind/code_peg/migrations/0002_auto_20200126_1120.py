# Generated by Django 2.2.9 on 2020-01-26 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("code_peg", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="codepeg",
            name="slot1",
            field=models.IntegerField(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
            ),
        ),
        migrations.AlterField(
            model_name="codepeg",
            name="slot2",
            field=models.IntegerField(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
            ),
        ),
        migrations.AlterField(
            model_name="codepeg",
            name="slot3",
            field=models.IntegerField(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
            ),
        ),
        migrations.AlterField(
            model_name="codepeg",
            name="slot4",
            field=models.IntegerField(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
            ),
        ),
    ]
