# -*- coding: utf-8 -*-
from django import forms
from account.models import Message
from teacher.models import Classroom, TWork
from student.models import Work, Enroll

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
           fields = ['score']
		   
        def __init__(self, user, *args, **kwargs): 
            super(ScoreForm, self).__init__(*args, **kwargs)
            self.initial['score'] = 100		
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

            