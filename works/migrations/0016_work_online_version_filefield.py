import works.storage_paths
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("works", "0015_work_volume_pages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="work",
            name="online_version_link",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=works.storage_paths.WorkOnlineVersionUploadPath(),
            ),
        ),
    ]
