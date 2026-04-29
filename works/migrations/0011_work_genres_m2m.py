from django.db import migrations, models


def _copy_genre_fk_to_m2m(apps, schema_editor) -> None:
    Work = apps.get_model("works", "Work")

    # Historical field exists on old state; ignore type checkers.
    for w in Work.objects.exclude(genre_id__isnull=True).only("id", "genre_id"):
        w.genres.add(w.genre_id)


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0010_rename_tables_to_work"),
    ]

    operations = [
        migrations.AddField(
            model_name="work",
            name="genres",
            field=models.ManyToManyField(blank=True, related_name="works", to="works.genre"),
        ),
        migrations.RunPython(_copy_genre_fk_to_m2m, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="work",
            name="genre",
        ),
    ]

