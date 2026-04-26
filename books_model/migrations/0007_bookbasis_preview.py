from django.db import migrations, models

import books_model.storage_paths


class Migration(migrations.Migration):
    dependencies = [
        ("books_model", "0006_bookbasis_authors_m2m"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookbasis",
            name="preview",
            field=models.ImageField(blank=True, null=True, upload_to=books_model.storage_paths.BookPreviewUploadPath()),
        ),
    ]

