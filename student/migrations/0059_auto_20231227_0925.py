# Generated by Django 4.2.8 on 2023-12-27 01:25
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0058_remove_enroll_classroom_id_remove_enroll_student_id_and_more'),
    ]

    operations = [
        #--------------------------------------------------------------------
        # WorkAssistant
        migrations.RunSQL(
            "DELETE FROM student_workassistant WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='workassistant',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='workassistant',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assistant_works', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunSQL(
            "DELETE FROM student_workassistant WHERE classroom_id not in (SELECT id from teacher_classroom)",
        ),
        migrations.RenameField(
            model_name='workassistant',
            old_name='classroom_id',
            new_name = 'classroom',
        ),
        migrations.AlterField(
            model_name='workassistant',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_assistants', to='teacher.classroom'),
        ),
        #--------------------------------------------------------------------
        # Work
        migrations.RunSQL(
            "DELETE FROM student_work WHERE user_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='work',
            old_name='user_id',
            new_name = 'user',
        ),
        migrations.AlterField(
            model_name='work',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='work',
            name='scorer',
            field=models.IntegerField(null=True),
        ),
        migrations.RunSQL(
            "UPDATE student_work SET scorer=null WHERE scorer = 0",
        ),
        migrations.AlterField(
            model_name='work',
            name='scorer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # WorkFile
        migrations.RunSQL(
            "DELETE FROM student_workfile WHERE work_id not in (SELECT id from student_work)",
        ),
        migrations.RenameField(
            model_name='workfile',
            old_name='work_id',
            new_name = 'work',
        ),
        migrations.AlterField(
            model_name='workfile',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='student.work'),
        ),
        #--------------------------------------------------------------------
        # Answer
        migrations.RunSQL(
            "DELETE FROM student_answer WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='answer',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # Exam
        migrations.RunSQL(
            "DELETE FROM student_exam WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='exam',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='exam',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # SFWork
        migrations.RunSQL(
            "DELETE FROM student_sfwork WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='sfwork',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='sfwork',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sfwork_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunSQL(
            "DELETE FROM student_sfwork WHERE scorer not in (SELECT id from auth_user)",
        ),
        migrations.AlterField(
            model_name='sfwork',
            name='scorer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score_sfwork_list', to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # SFWork
        migrations.RunSQL(
            "DELETE FROM student_sfcontent WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='sfcontent',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='sfcontent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunSQL(
            "DELETE FROM student_sfcontent WHERE work_id not in (SELECT id from student_work)",
        ),
        migrations.RenameField(
            model_name='sfcontent',
            old_name='work_id',
            new_name = 'work',
        ),
        migrations.AlterField(
            model_name='sfcontent',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.work'),
        ),
        #--------------------------------------------------------------------
        # SFReply
        migrations.RunSQL(
            "DELETE FROM student_sfreply WHERE work_id not in (SELECT id from student_work)",
        ),
        migrations.RenameField(
            model_name='sfreply',
            old_name='work_id',
            new_name = 'work',
        ),
        migrations.AlterField(
            model_name='sfreply',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.work'),
        ),
        migrations.RunSQL(
            "DELETE FROM student_sfreply WHERE user_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='sfreply',
            old_name='user_id',
            new_name = 'user',
        ),
        migrations.AlterField(
            model_name='sfreply',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # Science1Question
        migrations.RunSQL(
            "DELETE FROM student_science1question WHERE work_id not in (SELECT id from student_work)",
        ),
        migrations.RenameField(
            model_name='science1question',
            old_name='work_id',
            new_name = 'work',
        ),
        migrations.AlterField(
            model_name='science1question',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.work'),
        ),
        #--------------------------------------------------------------------
        # Science1Work
        migrations.RunSQL(
            "DELETE FROM student_science1work WHERE question_id not in (SELECT id from student_science1question)",
        ),
        migrations.RenameField(
            model_name='science1work',
            old_name='question_id',
            new_name = 'question',
        ),
        migrations.AlterField(
            model_name='science1work',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.science1question'),
        ),
        migrations.RunSQL(
            "DELETE FROM student_science1work WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='science1work',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='science1work',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # Science1Content
        migrations.RunSQL(
            "DELETE FROM student_science1content WHERE work_id not in (SELECT id from student_work)",
        ),
        migrations.RenameField(
            model_name='science1content',
            old_name='work_id',
            new_name = 'work',
        ),
        migrations.AlterField(
            model_name='science1content',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.work'),
        ),
        #--------------------------------------------------------------------
        # Science2Json
        migrations.RunSQL(
            "DELETE FROM student_science2json WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='science2json',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='science2json',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # Science3Work
        migrations.RunSQL(
            "DELETE FROM student_science3work WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='science3work',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='science3work',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # Science4Work
        migrations.RunSQL(
            "DELETE FROM student_science4work WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='science4work',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='science4work',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # Science4Debug
        migrations.RunSQL(
            "DELETE FROM student_science4debug WHERE work3_id not in (SELECT id from student_science3work)",
        ),
        migrations.RenameField(
            model_name='science4debug',
            old_name='work3_id',
            new_name = 'work3',
        ),
        migrations.AlterField(
            model_name='science4debug',
            name='work3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.science3work'),
        ),
        #--------------------------------------------------------------------
        # Plant
        migrations.RunSQL(
            "DELETE FROM student_plant WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='plant',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # PlantLight
        migrations.RunSQL(
            "DELETE FROM student_plantlight WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='plantlight',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='plantlight',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        #--------------------------------------------------------------------
        # PlantPhoto
        migrations.RunSQL(
            "DELETE FROM student_plantphoto WHERE student_id not in (SELECT id from auth_user)",
        ),
        migrations.RenameField(
            model_name='plantphoto',
            old_name='student_id',
            new_name = 'student',
        ),
        migrations.AlterField(
            model_name='plantphoto',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]