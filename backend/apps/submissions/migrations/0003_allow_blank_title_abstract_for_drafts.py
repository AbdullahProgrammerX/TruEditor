"""
Allow blank title and abstract for draft submissions.

Before this change, title and abstract were required at the database level,
which prevented creating draft submissions (step 1 of the wizard).
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0002_alter_author_options_alter_submission_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='title',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Title of the manuscript',
                max_length=500,
                verbose_name='Title',
            ),
        ),
        migrations.AlterField(
            model_name='submission',
            name='abstract',
            field=models.TextField(
                blank=True,
                default='',
                help_text='Abstract of the manuscript (max 5000 characters)',
                max_length=5000,
                verbose_name='Abstract',
            ),
        ),
    ]
