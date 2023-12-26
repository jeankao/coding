# -*- coding: utf-8 -*-
from django import forms
from teacher.models import Classroom
from student.models import *

class EnrollForm(forms.Form):
    password =  forms.CharField()
    seat = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(EnrollForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = "選課密碼"
        self.fields['seat'].label = "座號"

# 組別人數
class GroupSizeForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['group_size']

    def __init__(self, *args, **kwargs):
        super(GroupSizeForm, self).__init__(*args, **kwargs)
        self.fields['group_size'].label = "小組人數"

class SeatForm(forms.ModelForm):
    class Meta:
        model = Enroll
        fields = ['seat']

class SubmitAForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['file','memo']

    def __init__(self, *args, **kwargs):
        super(SubmitAForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = "作品檔案"
        self.fields['memo'].label = "心得感想"

class SubmitBForm(forms.Form):
    HELP_CHOICES = [
        (0, "全部靠自己想"),
        (1, "同學幫一點忙"),
        (2, "同學幫很多忙"),
        (3, "解答幫一點忙"),
        (4, "解答幫很多忙"),
        (5, "老師幫一點忙"),
        (6, "老師幫很多忙"),
        ]
    code = forms.CharField(widget=forms.Textarea)
    screenshot = forms.CharField(widget=forms.HiddenInput())
    memo = forms.CharField(widget=forms.Textarea)
    helps = forms.ChoiceField(choices=HELP_CHOICES, required=True, label="程度", widget=forms.RadioSelect)

class SubmitCForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['youtube','memo']

    def __init__(self, *args, **kwargs):
        super(SubmitCForm, self).__init__(*args, **kwargs)
        self.fields['youtube'].label = "影片網址"
        self.fields['memo'].label = "心得感想"

class SubmitDForm(forms.Form):
    screenshot = forms.CharField(widget=forms.HiddenInput())
    memo = forms.CharField(widget=forms.Textarea)

# 新增一個作業
class SubmitF1Form(forms.ModelForm):
    class Meta:
        model = Science1Content
        fields = ['work_id', 'types', 'text', 'pic']

    def __init__(self, *args, **kwargs):
        super(SubmitF1Form, self).__init__(*args, **kwargs)
        self.fields['work_id'].required = False
        self.fields['types'].required = False
        self.fields['text'].required = False
        self.fields['pic'].required = False

# 資料建模，流程建模
class SubmitF2Form(forms.Form):
    jsonstr = forms.CharField(widget=forms.Textarea)

class SubmitF3Form(forms.Form):
    code = forms.CharField(widget=forms.Textarea)
    helps = forms.IntegerField()
    screenshot = forms.CharField(widget=forms.HiddenInput())

# 新增一個作業
class SubmitF4Form(forms.Form):
    index = forms.IntegerField(widget=forms.HiddenInput())
    memo = forms.CharField()

# 新增一個作業
class SubmitF4BugForm(forms.ModelForm):
    class Meta:
        model = Science4Debug
        fields = ['work3_id', 'bug_types', 'bug', 'improve']

    def __init__(self, *args, **kwargs):
        super(SubmitF4BugForm, self).__init__(*args, **kwargs)
        self.fields['work3_id'].required = False
        self.fields['bug_types'].required = False
        self.fields['bug'].required = False
        self.fields['improve'].required = False

class SubmitGForm(forms.Form):
    memo =  forms.CharField(required=False)
    memo_e =  forms.IntegerField(required=False)
    memo_c =  forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(SubmitGForm, self).__init__(*args, **kwargs)
        self.fields['memo'].label = "心得感想"
        self.fields['memo_e'].label = "英文"
        self.fields['memo_c'].label = "中文"

class ForumSubmitForm(forms.Form):
    memo =  forms.CharField(required=False)
    memo_e =  forms.IntegerField(required=False)
    memo_c =  forms.IntegerField(required=False)
    file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(ForumSubmitForm, self).__init__(*args, **kwargs)
        self.fields['memo'].label = "心得感想"
        self.fields['memo_e'].label = "英文"
        self.fields['memo_c'].label = "中文"
        self.fields['file'].label = "檔案"

class DataForm(forms.Form):
    name =  forms.CharField(required=False)
    index =  forms.IntegerField(widget=forms.HiddenInput())
    types =  forms.IntegerField(widget=forms.HiddenInput())

class PlantSubmitForm(forms.Form):
    memo =  forms.CharField(required=False)
    picture = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(PlantSubmitForm, self).__init__(*args, **kwargs)
        self.fields['memo'].label = "說明"

class PlantLightForm(forms.Form):
    light = forms.FloatField(required=False)
    password = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super(PlantLightForm, self).__init__(*args, **kwargs)


class PlantPhotoForm(forms.ModelForm):
    class Meta:
        model = PlantPhoto
        fields = ['uploads']
