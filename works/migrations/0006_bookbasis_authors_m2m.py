# Переход BookBasis.author (FK) → BookBasis.authors (M2M)

from django.db import migrations, models


def forwards_copy_fk_to_m2m(apps, schema_editor):
    BookBasis = apps.get_model('works', 'BookBasis')
    for bb in BookBasis.objects.all():
        aid = getattr(bb, 'author_id', None)
        if aid is not None:
            bb.authors.add(aid)


class Migration(migrations.Migration):
    dependencies = [
        ('authors', '0001_initial'),
        ('works', '0005_book_basis_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookbasis',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='book_bases', to='authors.author'),
        ),
        migrations.RunPython(forwards_copy_fk_to_m2m, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='bookbasis',
            name='author',
        ),
    ]

