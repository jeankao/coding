# -*- coding: UTF-8 -*-
from django import template
from account.models import MessagePoll, School
from student.models import Enroll, Work, WorkFile
from teacher.models import *
from show.models import ShowGroup, Round, ShowReview
from certificate.models import Certificate
from student.lesson import *
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

register = template.Library()

@register.filter
def modulo(num, val):
    return num % val
  
@register.filter(name="img")
def img(title):
    if title.startswith(u'[私訊]'):
        return "line"
    elif title.startswith(u'[公告]'):
        return "announce"
    elif u'擔任小老師' in title:
        return "assistant"
    elif u'設您為教師' in title:
        return "teacher"
    elif u'核發了一張證書給你' in title:
        return "certificate"
    else :
        return ""
      
@register.filter(name='unread') 
def unread(user_id):
    return MessagePoll.objects.filter(reader_id=user_id, read=False).count()      

@register.filter()
def to_int(value):
    return int(value)
  
@register.filter(name='week') 
def week(date_number):
    year = date_number / 10000
    month = (date_number - year * 10000) / 100
    day = date_number - year * 10000 - month * 100
    now = datetime(year, month, day, 8, 0, 0)
    return now.strftime("%A")  
  
@register.filter()
def classroom(user_id):
    if user_id > 0 :
        enrolls = Enroll.objects.filter(student_id=user_id).order_by("-id")
        if len(enrolls) > 0 :
            classroom_name = Classroom.objects.get(id=enrolls[0].classroom_id).name
        else :
            classroom_name = ""
        return classroom_name
    else : 
        return "匿名"
      
@register.filter(takes_context=True)
def realname(user_id):
    try: 
        user = User.objects.get(id=user_id)
        return user.first_name
    except ObjectDoesNotExist:
        pass
        return ""      

@register.filter(takes_context=True)
def realname2(user_id):
    try: 
        user = User.objects.get(id=user_id)
        return user.first_name.replace(user.first_name[1], "O")
    except ObjectDoesNotExist:
        pass
        return ""  
      
@register.simple_tag
def work_name(index, lesson, typing):
  if typing == 1:
    return "自-" + TWork.objects.get(id=index).title
  elif typing == 2:
    return "檢-" + CWork.objects.get(id=index).title
  else :
    if lesson == 1:
        return lesson_list1[index-1][2]
    elif lesson == 2:
        return lesson_list2[index-1][1]
    elif lesson == 3:
        return lesson_list3[index-1][1]
    elif lesson == 4:
        return lesson_list4[index-1][1]
    else :
        return lesson_list1[index-1][2]
     
@register.filter(takes_context=True)
def school(school_id):
    if not school_id:
        return ""
    try: 
        school_name = School.objects.get(id=school_id).name
    except ObjectDoesNotExist:
        school_name = ""
    return school_name
      
@register.filter(name='has_group') 
def has_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name) 
    except ObjectDoesNotExist:
        group = None
    return group in user.groups.all()
  
@register.filter
def subtract(a, b):
    return a - b
  
@register.filter
def hash_memo(h, key):
    key = int(key)
    if key in h:
      return h[key][0].memo
    else:
      return ""

@register.filter
def hash_youtube(h, key):
    key = int(key)
    if key in h:
      return h[key][0].youtube
    else:
      return ""
    
@register.filter
def video(url):
    number_pos = url.find("v=")
    number = url[number_pos+2:number_pos+13]
    return number   
    
@register.filter
def hash_code(h, key):
    key = int(key)
    if key in h:
      return h[key][0].code
    else:
      return ""
    
@register.filter
def hash_helps(h, key):
    key = int(key)
    if key in h:
      return h[key][0].helps
    else:
      return -1
    
@register.filter
def hash_score(h, key):
    key = int(key)
    if key in h:
      return h[key][0].score
    else:
      return -1  
    
@register.filter
def hash_date(h, key):
    key = int(key)
    if key in h:
      return h[key][0].publication_date
    else:
      return False
    
@register.filter
def hash_scorer(h, key):
    key = int(key)
    if key in h:
      return h[key][0].scorer
    else:
      return 0
    
@register.filter
def hash_workid(h, key):
    key = int(key)
    if key in h:
      return h[key][0].id
    else:
      return 0    
    
@register.filter
def hash_file(h, key):
    key = int(key)
    if key in h:
      if len(h[key][1])>0:
        return h[key][1][0].filename
      else:
        return None
    else:
      return None
    
@register.filter
def hash_files(h, key):
    key = int(key)
    if key in h:
      if len(h[key][1])>0:
        return h[key][1]
      else:
        return None
    else:
      return None

@register.filter
def hash_picture(h, key):
    key = int(key)
    if key in h:
        return h[key][0].picture
    return None
    
@register.filter
def student_username(name):
    start = "_"
    student = name[name.find(start)+1:]
    return student    
  
@register.filter
def code_highlight(code):  
    html_code = highlight(code, PythonLexer(), HtmlFormatter(linenos=True))
    return html_code
  
@register.filter
def hoc(user_id):  
    try:
        certificate = Certificate.objects.get(student_id=user_id)
        return "<img src=/static/certification/1/0/"+str(user_id)+".jpg>"
    except ObjectDoesNotExist:     
        return ""
      
@register.filter()
def show_member(show_id):
    members = Enroll.objects.filter(groupshow__icontains=str(show_id)+",")
    name = ""
    for member in members:
        name = name + '<' + member.student.first_name + '>'
    return name
  
@register.filter()
def show_teacher(show_id):
    show = ShowGroup.objects.get(id=show_id)
    round = Round.objects.get(id=show.round_id)
    classroom = Classroom.objects.get(id=round.classroom_id)
    teacher = User.objects.get(id=classroom.teacher_id)
    school = School.objects.get(id=teacher.last_name).name
    return "<" + school + "><" + teacher.first_name + u"老師>"
  
@register.filter()
def show_category(show_id):
    show = ShowGroup.objects.get(id=show_id)
    round = Round.objects.get(id=show.round_id)
    classroom = Classroom.objects.get(id=round.classroom_id)
    if classroom.lesson == 1:
        return 1
    else :
        return 2
      
@register.filter()
def review_score(show_id, user_id):
    show_review = ShowReview.objects.get(show_id=show_id, student_id=user_id)
    return show_review.score
  
@register.filter()
def is_pic(title):   
    if title[-3:].upper() == "PNG":
        return True
    if title[-3:].upper() == "JPG":
        return True   
    if title[-3:].upper() == "GIF":
        return True            
    return False
 
	
@register.filter(name='abs_filter')
def abs_filter(value):
    return abs(value)
  
@register.filter(name='assistant') 
def assistant(user_id):
    assistants = Assistant.objects.filter(user_id=user_id)
    if assistants:
      return True
    return False