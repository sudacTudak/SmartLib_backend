from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0009_rename_book_models_to_work"),
    ]

    operations = [
        migrations.AlterModelTable(name="work", table="work"),
        migrations.AlterModelTable(name="workitem", table="work_item"),
    ]

