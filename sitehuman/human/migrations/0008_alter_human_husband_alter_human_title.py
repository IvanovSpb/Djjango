# Generated by Django 4.2.1 on 2025-03-17 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("human", "0007_husband_alter_human_tags_human_husband"),
    ]

    operations = [
        migrations.AlterField(
            model_name="human",
            name="husband",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="husband",
                to="human.husband",
            ),
        ),
        migrations.AlterField(
            model_name="human",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Заголовок"),
        ),
    ]
