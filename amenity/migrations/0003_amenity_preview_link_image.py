from django.db import migrations, models

import amenity.storage_paths


class Migration(migrations.Migration):
    dependencies = [
        ("amenity", "0002_amenityvendorviewset"),
    ]

    operations = [
        migrations.AlterField(
            model_name="amenity",
            name="preview_link",
            field=models.ImageField(blank=True, null=True, upload_to=amenity.storage_paths.AmenityPreviewUploadPath()),
        ),
    ]

