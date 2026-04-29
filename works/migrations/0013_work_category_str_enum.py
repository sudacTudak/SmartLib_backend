from django.db import migrations, models

from works.enums import WorkCategory


INT_TO_STR = {
    0: "book",
    1: "scientific_article",
    2: "collected_articles",
    3: "journal",
    4: "comic",
    5: "lecture_notes",
}


def _copy_int_category_to_str(apps, schema_editor) -> None:
    Work = apps.get_model("works", "Work")
    for w in Work.objects.all().only("id", "category"):
        # `category` here is int (from 0012); `category_tmp` is the new str field.
        w.category_tmp = INT_TO_STR.get(w.category, "book")
        w.save(update_fields=["category_tmp"])


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0012_work_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="work",
            name="category_tmp",
            field=models.CharField(
                max_length=32,
                choices=WorkCategory.as_django_model_choices(),
                default="book",
            ),
        ),
        migrations.RunPython(_copy_int_category_to_str, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="work",
            name="category",
        ),
        migrations.RenameField(
            model_name="work",
            old_name="category_tmp",
            new_name="category",
        ),
    ]

