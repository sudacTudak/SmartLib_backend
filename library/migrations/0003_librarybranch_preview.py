from django.db import migrations, models

import library.storage_paths


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0002_alter_librarybranch_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="librarybranch",
            name="preview",
            field=models.ImageField(blank=True, null=True, upload_to=library.storage_paths.LibraryPreviewUploadPath()),
        ),
    ]

