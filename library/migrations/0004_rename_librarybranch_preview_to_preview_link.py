from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0003_librarybranch_preview"),
    ]

    operations = [
        migrations.RenameField(
            model_name="librarybranch",
            old_name="preview",
            new_name="preview_link",
        ),
    ]

