from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0008_rename_bookbasis_preview_to_preview_link"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="BookBasis",
            new_name="Work",
        ),
        migrations.RenameModel(
            old_name="Book",
            new_name="WorkItem",
        ),
        migrations.RemoveConstraint(
            model_name="workitem",
            name="unique_book_basis_per_library_branch",
        ),
        migrations.RenameField(
            model_name="workitem",
            old_name="book_basis",
            new_name="work",
        ),
        migrations.AddConstraint(
            model_name="workitem",
            constraint=models.UniqueConstraint(
                fields=("work", "library_branch"),
                name="unique_book_basis_per_library_branch",
            ),
        ),
    ]

