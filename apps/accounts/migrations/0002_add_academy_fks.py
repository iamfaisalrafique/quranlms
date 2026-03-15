"""
accounts 0002 — add academy FK to StudentProfile and TeacherProfile.
Runs AFTER academy.0002 (which adds the owner FK, ensuring User exists first).
"""
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('academy', '0002_initial'),   # safe now: academy.0002 depends on accounts.0001's User
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='academy',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='students',
                to='academy.academy',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='academy',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='teachers',
                to='academy.academy',
            ),
            preserve_default=False,
        ),
    ]
