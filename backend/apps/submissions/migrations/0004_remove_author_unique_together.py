"""
Remove unique_together constraint from Author model.
The order field is managed at application level.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0003_allow_blank_title_abstract_for_drafts'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='author',
            unique_together=set(),
        ),
    ]
