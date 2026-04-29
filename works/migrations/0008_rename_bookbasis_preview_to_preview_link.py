from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0007_bookbasis_preview"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bookbasis",
            old_name="preview",
            new_name="preview_link",
        ),
    ]

