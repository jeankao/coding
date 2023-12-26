# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# 班級
class Classroom(models.Model):
    Lesson_CHOICES = [
        (1, '程式設計輕鬆學：使用Scratch2.X'),
        (2, 'VPhyscis物理模擬：使用Python2'),
        (3, 'Euler數學解題：使用Python3'),
        (4, 'VPhyscis物理模擬：建中特色課程'),
        (5, 'VPhyscis物理模擬：使用Python3'),
        (6, '機器人程式設計：使用Microbit'),
        (7, 'Pandas數據分析：使用Python3'),
        (8, 'Django網站開發：使用Python3'),
        (9, 'Science科學運算：使用Python3'),
        (10, '網路讀書會：好書共讀'),
		]

    LessonShort_CHOICES = [
        (1, 'Scratch'),
        (2, 'VPhyscis2'),
        (3, 'Euler'),
        (4, 'VPhysics-CK'),
        (5, 'VPhysics3'),
        (6, 'Microbit'),
        (7, 'Pandas'),
        (8, 'Django'),
        (9, 'Science'),
        (10, 'Book'),
		]
    # 班級名稱
    name = models.CharField(max_length=30)
    # 課程名稱
    lesson = models.IntegerField(default=0, choices=Lesson_CHOICES)
    # 選課密碼
    password = models.CharField(max_length=30)
    # 授課教師
    teacher_id = models.IntegerField(default=0)
    # 是否開放分組
    group_open = models.BooleanField(default=True)
    # 組別數目
    group_number = models.IntegerField(default=8)
    # 組別人數
    group_size = models.IntegerField(default=4)
    # 是否開放創意秀分組
    group_show_open = models.BooleanField(default=False)
    # 組別人數
    group_show_size = models.IntegerField(default=2)
	# 事件
    event_open = models.BooleanField(default=True)
	# 課程事件
    event_video_open = models.BooleanField(default=True)

    @property
    def teacher(self):
        return User.objects.get(id=self.teacher_id)

    def __unicode__(self):
        return self.name

    def lesson_choice(self):
        return dict(Classroom.LessonShort_CHOICES)[self.lesson]

    def __str__(self):
        return "{}({})".format(self.name, dict(self.LessonShort_CHOICES)[self.lesson])

#匯入
class ImportUser(models.Model):
	username = models.CharField(max_length=50, default="")
	first_name = models.CharField(max_length=50, default="")
	password = models.CharField(max_length=50, default="")
	email = models.CharField(max_length=100, default="")

#自訂作業
class TWork(models.Model):
    title = models.CharField(max_length=250)
    classroom_id = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)

#檢核作業
class CWork(models.Model):
    title = models.CharField(max_length=250)
    classroom_id = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)


#班級助教
class Assistant(models.Model):
    classroom_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)

#討論區
class FWork(models.Model):
    title = models.CharField(max_length=250,verbose_name= '討論主題')
    teacher_id = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
    domains = models.TextField(default='')
    levels = models.TextField(default='')

def get_deadline():
    return datetime.today() + timedelta(days=14)

class FClass(models.Model):
    forum_id = models.IntegerField(default=0)
    classroom_id =  models.IntegerField(default=0)
    publication_date = models.DateTimeField(default=timezone.now)
    deadline = models.BooleanField(default=False)
    deadline_date = models.DateTimeField(default=get_deadline)

    def __unicode__(self):
        return str(self.forum_id)

class FContent(models.Model):
    forum_id =  models.IntegerField(default=0)
    types = models.IntegerField(default=0)
    title = models.CharField(max_length=250,null=True,blank=True)
    memo = models.TextField(default='')
    link = models.CharField(max_length=250,null=True,blank=True)
    youtube = models.CharField(max_length=250,null=True,blank=True)
    youtube_length = models.IntegerField(default=0)
    file = models.FileField(blank=True,null=True)
    filename = models.CharField(max_length=60,null=True,blank=True)
