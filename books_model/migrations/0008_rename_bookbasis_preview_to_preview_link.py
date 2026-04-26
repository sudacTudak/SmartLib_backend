from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books_model", "0007_bookbasis_preview"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bookbasis",
            old_name="preview",
            new_name="preview_link",
        ),
    ]

