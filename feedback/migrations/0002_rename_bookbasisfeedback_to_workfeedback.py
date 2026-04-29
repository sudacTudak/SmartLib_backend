from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="BookBasisFeedback", new_name="WorkFeedback"),
        migrations.AlterModelTable(name="workfeedback", table="work_feedback"),
    ]

