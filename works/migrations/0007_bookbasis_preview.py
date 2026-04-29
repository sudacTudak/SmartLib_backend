from django.db import migrations, models

import works.storage_paths


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0006_bookbasis_authors_m2m"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookbasis",
            name="preview",
            field=models.ImageField(blank=True, null=True, upload_to=works.storage_paths.WorkPreviewUploadPath()),
        ),
    ]

