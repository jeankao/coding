# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class County(models.Model):
  name = models.CharField(max_length=20)
  mapx = models.IntegerField(default=0)	
  mapy = models.IntegerField(default=0)	
    
class Zone(models.Model):
  name = models.CharField(max_length=20)
  county = models.IntegerField(default=0)

class School(models.Model):
  county = models.IntegerField(default=0)
  zone = models.IntegerField(default=0)
  system = models.IntegerField(default=0)
  name = models.CharField(max_length=50)
  online = models.BooleanField(default=True)
    
# 個人檔案資料
class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name="profile")
	# 積分：上傳作業
  work = models.IntegerField(default=0)
	# 積分：擔任小老師
  assistant = models.IntegerField(default=0)
	# 積分：創意秀
  creative = models.IntegerField(default=0)	
	# 大頭貼等級
  avatar = models.IntegerField(default=0)
	# 訪客人次
  home_count = models.IntegerField(default=0)
  visitor_count = models.IntegerField(default=0)
	# 開站時間
  open_time = models.DateTimeField(auto_now_add=True)

# 積分記錄 
class PointHistory(models.Model):
    # 使用者序號
	user_id = models.IntegerField(default=0)
	# 積分類別 1:上傳作業 2:小老師
	kind = models.IntegerField(default=0)
	# 積分項目
	message = models.CharField(max_length=100)	
	# 將積分項目超連結到某個頁面
	url = models.CharField(max_length=100)
	# 記載時間 
	publish = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return str(self.user_id)
  
# 大廳訊息	
class Message(models.Model):
    author_id = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    title = models.CharField(max_length=250)
    content = models.TextField(default='')
    url = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)
	
    @classmethod
    def create(cls, title, url, time):
        message = cls(title=title, url=url, time=time)
        return message

# 訊息    
class MessagePoll(models.Model):
    message_id = models.IntegerField(default=0)
    reader_id = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    read = models.BooleanField(default=False)
    
    @property
    def message(self):
        return Message.objects.get(id=self.message_id)        

class MessageFile(models.Model):
    message_id = models.IntegerField(default=0) 
    filename = models.TextField()
    before_name = models.TextField()
    upload_date = models.DateTimeField(default=timezone.now)

class MessageContent(models.Model):
    message_id =  models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    title =  models.CharField(max_length=250,null=True,blank=True)
    filename = models.CharField(max_length=250,null=True,blank=True)    
    publication_date = models.DateTimeField(default=timezone.now)

# 訪客 
class Visitor(models.Model):
    date = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    
# 訪客記錄
class VisitorLog(models.Model):
    visitor_id = models.IntegerField(default=0)    
    user_id = models.IntegerField(default=0)
    IP = models.CharField(max_length=20, default="")
    time = models.DateTimeField(auto_now_add=True)		    
		
#課程計數器
class LessonCounter(models.Model):
	name = models.CharField(max_length=10)
	hit = models.IntegerField(default=0)
	
#日期計數器
class DayCounter(models.Model):
	day = models.CharField(max_length=8)
	hit = models.IntegerField(default=0)	
	
#計數器記錄
class LogCounter(models.Model):
	counter_id = models.IntegerField(default=0)
	counter_date = models.DateTimeField(default=timezone.now)
	counter_ip = models.CharField(max_length=20)