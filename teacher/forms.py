# -*- coding: utf-8 -*-
from django import forms
from account.models import Message
from teacher.models import Classroom, TWork, CWork, FWork, FClass, FContent
from student.models import *

# 新增一個課程表單
class ClassroomForm(forms.ModelForm):
        class Meta:
           model = Classroom
           fields = ['lesson', 'name', 'password']
        
        def __init__(self, *args, **kwargs):
            super(ClassroomForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = "班級名稱"
            self.fields['lesson'].label = "課程名稱"			
            self.fields['password'].label = "選課密碼"

            
# 新增一個課程表單
class AnnounceForm(forms.ModelForm):
        class Meta:
           model = Message
           fields = ['title','content']
        
        def __init__(self, *args, **kwargs):
            super(AnnounceForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "公告主旨"
            self.fields['title'].widget.attrs['size'] = 50
            self.fields['content'].label = "公告內容"
            self.fields['content'].widget.attrs['cols'] = 50
            self.fields['content'].widget.attrs['rows'] = 20 
            
# 作業評分表單           
class ScoreForm(forms.ModelForm):
        RELEVANCE_CHOICES = (
            (100, "你好棒(100分)"),
            (90, "90分"),
            (80, "80分"),
            (70, "70分"),
            (60, "60分"),
			(-1, "重交")
        )
        score = forms.ChoiceField(choices = RELEVANCE_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        assistant = forms.BooleanField(required=False,label="小老師")
    
        class Meta:
           model = Work
           fields = ['score', 'comment']
		   
        def __init__(self, user, *args, **kwargs): 
            super(ScoreForm, self).__init__(*args, **kwargs)
            self.fields['comment'].required = False			
            self.initial['score'] = 100		
            if user.groups.all().count() == 0 :
                del self.fields['assistant']
                
# 作業評分表單           
class ScoreBForm(forms.ModelForm):
        RELEVANCE_CHOICES = (
            (10, "10分"),
            (9, "9分"),
            (8, "8分"),
            (7, "7分"),
            (6, "6分"),
            (5, "5分"),
            (4, "4分"),
            (3, "3分"),
            (2, "2分"),
            (1, "1分"),          
			(-1, "重交")
        )
        score = forms.ChoiceField(choices = RELEVANCE_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        assistant = forms.BooleanField(required=False,label="小老師")
    
        class Meta:
           model = Work
           fields = ['score']
		   
        def __init__(self, user, *args, **kwargs): 
            super(ScoreBForm, self).__init__(*args, **kwargs)
            self.initial['score'] = 10		
            if user.groups.all().count() == 0 :
                del self.fields['assistant']
                
			
#上傳檔案
class UploadFileForm(forms.Form):
    file = forms.FileField()

Check_CHOICES = (
    (100, "你好棒(100分)"),
    (90, "90分"),
    (80, "80分"),
    (70, "70分"),
    (60, "60分"),
    (40, "40分"),
    (20, "20分"),
    (0, "0分"),			
)    

    
class CheckForm(forms.ModelForm):
        score_memo = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
    
        class Meta:
           model = Enroll
           fields = ['score_memo']
    
class CheckForm1(forms.ModelForm):

        score_memo1 = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        certificate = forms.BooleanField(required=False,label="核發證書",initial=True)
    
        class Meta:
           model = Enroll
           fields = ['score_memo1']

class CheckForm2(forms.ModelForm):

        score_memo2 = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        certificate = forms.BooleanField(required=False,label="核發證書",initial=True)
    
        class Meta:
           model = Enroll
           fields = ['score_memo2']

class CheckForm3(forms.ModelForm):

        score_memo3 = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        certificate = forms.BooleanField(required=False,label="核發證書",initial=True)
    
        class Meta:
           model = Enroll
           fields = ['score_memo3']

class CheckForm4(forms.ModelForm):
        score_memo4 = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        certificate = forms.BooleanField(required=False,label="核發證書",initial=True)
    
        class Meta:
           model = Enroll
           fields = ['score_memo4']
            
class CheckForm_vphysics(forms.ModelForm):
        score_memo_vphysics = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        certificate = forms.BooleanField(required=False,label="核發證書",initial=True)
    
        class Meta:
           model = Enroll
           fields = ['score_memo_vphysics']          

class CheckForm_euler(forms.ModelForm):
        score_memo_euler = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        certificate = forms.BooleanField(required=False,label="核發證書",initial=True)
    
        class Meta:
           model = Enroll
           fields = ['score_memo_euler']                

# 新增一個作業
class WorkForm(forms.ModelForm):
        class Meta:
           model = TWork
           fields = ['title']
        
        def __init__(self, *args, **kwargs):
            super(WorkForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "作業名稱"
            
# 新增一個作業
class Work3Form(forms.ModelForm):
        class Meta:
           model = CWork
           fields = ['title']
        
        def __init__(self, *args, **kwargs):
            super(Work3Form, self).__init__(*args, **kwargs)
            self.fields['title'].label = "作業名稱"            

# 新增一個課程表單
class ForumCategroyForm(forms.ModelForm):
        class Meta:
           model = FWork
           fields = ['domains', 'levels']
        
        def __init__(self, *args, **kwargs):
            super(ForumCategroyForm, self).__init__(*args, **kwargs)			
						
# 新增一個繳交期長表單
class ForumDeadlineForm(forms.ModelForm):
        class Meta:
           model = FClass
           fields = ['deadline', 'deadline_date']
        
        def __init__(self, *args, **kwargs):
            super(ForumDeadlineForm, self).__init__(*args, **kwargs)			

						
# 新增一個作業
class ForumForm(forms.ModelForm):
        class Meta:
           model = FWork
           fields = ['title']
        
        def __init__(self, *args, **kwargs):
            super(ForumForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "討論主題"
            self.fields['title'].widget.attrs.update({'class' : 'form-control list-group-item-text'})									
						
# 新增一個作業
class ForumContentForm(forms.ModelForm):
        class Meta:
           model = FContent
           fields = ['forum_id', 'types', 'title', 'link', 'youtube', 'file', 'memo']
        
        def __init__(self, *args, **kwargs):
            super(ForumContentForm, self).__init__(*args, **kwargs)
            self.fields['forum_id'].required = False		
            self.fields['title'].required = False						
            self.fields['link'].required = False
            self.fields['youtube'].required = False
            self.fields['file'].required = False
            self.fields['memo'].required = False						
						
            
# 新增一個作業
class QuestionForm(forms.ModelForm):
        class Meta:
           model = Science1Question
           fields = ['question']
        
        def __init__(self, *args, **kwargs):
            super(QuestionForm, self).__init__(*args, **kwargs)
            self.fields['question'].label = "問題"