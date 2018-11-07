# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from teacher.models import Classroom
from django.utils import timezone
from django.core.validators import RegexValidator, validate_comma_separated_integer_list

# 學生選課資料
class Enroll(models.Model):
    # 學生序號
    student_id = models.IntegerField(default=0)
    # 班級序號
    classroom_id = models.IntegerField(default=0)
    # 座號
    seat = models.IntegerField(default=0)
    # 組別
    group = models.IntegerField(default=0)
    # 創意秀組別
    #groupshow = models.CommaSeparatedIntegerField(max_length=200)
    groupshow = models.CharField(validators=[validate_comma_separated_integer_list], max_length=200)
    # 12堂課證書
    certificate1 = models.BooleanField(default=False)
    certificate1_date = models.DateTimeField(default=timezone.now)
    # 實戰入門證書
    certificate2 = models.BooleanField(default=False)
    certificate2_date = models.DateTimeField(default=timezone.now)
    # 實戰進擊證書
    certificate3 = models.BooleanField(default=False)
    certificate3_date = models.DateTimeField(default=timezone.now)
    # 實戰高手證書
    certificate4 = models.BooleanField(default=False)
    certificate4_date = models.DateTimeField(default=timezone.now)

    # 自訂作業
    score_memo = models.IntegerField(default=0)
    # 12堂課 心得成績
    score_memo1 = models.IntegerField(default=0)
    # 實戰入門心得成績
    score_memo2 = models.IntegerField(default=0)
    # 實戰進擊心得成績
    score_memo3 = models.IntegerField(default=0)
    # 實戰高手心得成績
    score_memo4 = models.IntegerField(default=0)
    # Vphysics2
    certificate_vphysics = models.BooleanField(default=False)
    certificate_vphysics_date = models.DateTimeField(default=timezone.now)
    score_memo_vphysics =  models.IntegerField(default=0)
    # Euler
    certificate_euler = models.BooleanField(default=False)
    certificate_euler_date = models.DateTimeField(default=timezone.now)
    score_memo_euler =  models.IntegerField(default=0)
    # Vphysics CK
    certificate_vphysics2 = models.BooleanField(default=False)
    certificate_vphysics2_date = models.DateTimeField(default=timezone.now)
    score_memo_vphysics2 =  models.IntegerField(default=0)
    # Vphysics3
    certificate_vphysics3 = models.BooleanField(default=False)
    certificate_vphysics3_date = models.DateTimeField(default=timezone.now)
    score_memo_vphysics3 =  models.IntegerField(default=0)
    # Microbit
    certificate_microbit = models.BooleanField(default=False)
    certificate_microbit_date = models.DateTimeField(default=timezone.now)
    score_memo_microbit =  models.IntegerField(default=0)
    # 自訂作業
    score_memo_custom =  models.IntegerField(default=0)
    # 檢核作業
    score_memo_check =  models.IntegerField(default=0)

    @property
    def classroom(self):
        return Classroom.objects.get(id=self.classroom_id)

    @property
    def student(self):
        return User.objects.get(id=self.student_id)

    def __str__(self):
        return str(self.id) + ":" + str(self.classroom_id)

    class Meta:
        unique_together = ('student_id', 'classroom_id',)

    def set_foo(self, x):
        self.groupshow = json.dumps(x)

    def get_groupshow(self):
        return json.loads(self.groupshow)

# 學生組別
class EnrollGroup(models.Model):
    name = models.CharField(max_length=30)
    classroom_id = models.IntegerField(default=0)

# 小老師
class WorkAssistant(models.Model):
    student_id = models.IntegerField(default=0)
    typing = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    index = models.IntegerField(default=0)
    lesson_id = models.IntegerField(default=0)

    @property
    def student(self):
        return User.objects.get(id=self.student_id)

def upload_path_handler(instance, filename):
    return "static/certificate/0/{filename}".format(filename=instance.id+".jpg")

class Work(models.Model):
    HELP_CHOICES = [
            (0, "全部靠自己想"),
            (1, "同學幫一點忙"),
            (2, "同學幫很多忙"),
            (3, "解答幫一點忙"),
            (4, "解答幫很多忙"),
            (5, "老師幫一點忙"),
            (6, "老師幫很多忙"),
		]

    user_id = models.IntegerField(default=0)
    lesson_id = models.IntegerField(default=0)
    typing = models.IntegerField(default=0)
    index = models.IntegerField()
    memo = models.TextField()
    publication_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=-2)
    scorer = models.IntegerField(default=0)
		# scratch, microbit
    file = models.FileField()
		#python
    picture = models.ImageField(upload_to = upload_path_handler, default = '/static/python/null.jpg')
    code = models.TextField(default='')
    helps = models.IntegerField(default=0, choices=HELP_CHOICES)
    answer = models.BooleanField(default=False)
    youtube = models.TextField(default='')
    comment = models.TextField(default='')

    def __unicode__(self):
        user = User.objects.filter(id=self.user_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"

    @property
    def user(self):
        return User.objects.get(id=self.user_id)

class WorkFile(models.Model):
    work_id = models.IntegerField(default=0)
    filename = models.TextField()
    upload_date = models.DateTimeField(default=timezone.now)

#解答
class Answer(models.Model):
    student_id = models.IntegerField(default=0)
    lesson_id = models.IntegerField(default=0)
    index = models.IntegerField()

    def __unicode__(self):
        user = User.objects.filter(id=self.student_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"

# 測驗
class Exam(models.Model):
    exam_id = models.IntegerField()
    student_id = models.IntegerField()
    answer = models.TextField()
    score = models.IntegerField()
    test_time = models.DateTimeField(default=timezone.now)

#討論區作業
class SFWork(models.Model):
    student_id = models.IntegerField(default=0)
    index = models.IntegerField()
    memo = models.TextField(default='')
    memo_e =  models.IntegerField(default=0)
    memo_c = models.IntegerField(default=0)
    publish = models.BooleanField(default=False)
    publication_date = models.DateTimeField(default=timezone.now)
    reply_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0)
    scorer = models.IntegerField(default=0)
    comment = models.TextField(default='',null=True,blank=True)
    comment_publication_date = models.DateTimeField(default=timezone.now)
    likes = models.TextField(default='')
    like_count = models.IntegerField(default=0)
    reply = models.IntegerField(default=0)

    def __unicode__(self):
        user = User.objects.filter(id=self.student_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"

class SFContent(models.Model):
    index =  models.IntegerField(default=0)
    student_id = models.IntegerField(default=0)
    work_id = models.IntegerField(default=0)
    title =  models.CharField(max_length=250,null=True,blank=True)
    filename = models.CharField(max_length=60,null=True,blank=True)
    publication_date = models.DateTimeField(default=timezone.now)
    delete_date = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)

#討論留言
class SFReply(models.Model):
    index = models.IntegerField(default=0)
    work_id =  models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    memo =  models.TextField(default='')
    publication_date = models.DateTimeField(default=timezone.now)

#Science1現象
class Science1Question(models.Model):
    work_id = models.IntegerField(default=0)
    question =  models.TextField(default='')

class Science1Work(models.Model):
    question_id = models.IntegerField(default=0)
    student_id = models.IntegerField(default=0)
    index = models.IntegerField(default=0)
    publication_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        user = User.objects.filter(id=self.student_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"

class Science1Content(models.Model):
    work_id =  models.IntegerField(default=0)
    types = models.IntegerField(default=0)
    text = models.TextField(default='')
    pic = models.FileField(blank=True,null=True)
    picname = models.CharField(max_length=60,null=True,blank=True)

#Science4解釋
class Science4Work(models.Model):
    student_id = models.IntegerField(default=0)
    index = models.IntegerField(default=0)
    publication_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        user = User.objects.filter(id=self.student_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"

class Science4Content(models.Model):
    work_id =  models.IntegerField(default=0)
    types = models.IntegerField(default=0)
    text = models.TextField(default='')
    pic = models.FileField(blank=True,null=True)
    picname = models.CharField(max_length=60,null=True,blank=True)

class Science3Work(models.Model):
    student_id = models.IntegerField(default=0)
    lesson = models.IntegerField(default=0)
    typing = models.IntegerField(default=0)
    index = models.IntegerField()
    publication_date = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to = upload_path_handler, default = '/static/python/null.jpg')
    code = models.TextField(default='')

    def __unicode__(self):
        user = User.objects.filter(id=self.user_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"

# 資料建模，流程建模
class Science2Json(models.Model):
    index = models.IntegerField(default=0)
    student_id = models.IntegerField(default=0)
    model_type = models.IntegerField(default=0) # 0: 資料建模, 1: 流程建模
    json = models.TextField(default='')