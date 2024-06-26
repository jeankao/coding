# Generated by Django 4.2.8 on 2023-12-13 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0025_alter_county_id_alter_daycounter_id_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "DELETE FROM account_log WHERE user_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='log',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RunSQL(
            "DELETE FROM account_pointhistory WHERE user_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='pointhistory',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RunSQL(
            "DELETE FROM account_visitorlog WHERE user_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='visitorlog',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='log',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vid_log', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pointhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='point_history', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='visitorlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit_log', to=settings.AUTH_USER_MODEL),
        ),
    ]
