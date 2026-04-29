from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0011_work_genres_m2m"),
    ]

    operations = [
        migrations.AddField(
            model_name="work",
            name="category",
            field=models.PositiveSmallIntegerField(
                choices=(
                    (0, "Book"),
                    (1, "ScientificArticle"),
                    (2, "CollectedArticles"),
                    (3, "Journal"),
                    (4, "Comic"),
                    (5, "LectureNotes"),
                ),
                default=0,
            ),
            preserve_default=False,
        ),
    ]

