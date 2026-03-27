import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0006_correspondence"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="verification_status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("verified", "Verified"),
                    ("declined", "Declined"),
                    ("not_required", "Not Required"),
                ],
                default="not_required",
                help_text="Co-author contribution verification status",
                max_length=20,
                verbose_name="Verification Status",
            ),
        ),
        migrations.AddField(
            model_name="author",
            name="verification_token",
            field=models.UUIDField(
                default=uuid.uuid4,
                help_text="Token for email-based verification link",
                unique=True,
                verbose_name="Verification Token",
            ),
        ),
        migrations.AddField(
            model_name="author",
            name="verified_at",
            field=models.DateTimeField(
                blank=True,
                help_text="When the co-author verified their contribution",
                null=True,
                verbose_name="Verified At",
            ),
        ),
        migrations.AddField(
            model_name="author",
            name="notified_at",
            field=models.DateTimeField(
                blank=True,
                help_text="When the co-author was last notified",
                null=True,
                verbose_name="Notified At",
            ),
        ),
        migrations.AddIndex(
            model_name="author",
            index=models.Index(
                fields=["user", "verification_status"],
                name="submissions_user_id_verific_idx",
            ),
        ),
    ]
