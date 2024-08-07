# -*- coding: utf-8 -*-
from django import forms
from show.models import ShowGroup, ShowReview
from teacher.models import Classroom
#from django.views.generic.edit import UpdateView

# 組別
class GroupForm(forms.ModelForm):
        class Meta:
           model = ShowGroup
           fields = ['name']

        def __init__(self, *args, **kwargs):
            super(GroupForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = "組別名稱"

# Scratch作品
class ShowForm1(forms.ModelForm):
        class Meta:
           model = ShowGroup
           fields = ['file','site','title','body', 'youtube']

        def __init__(self, *args, **kwargs):
            super(ShowForm1, self).__init__(*args, **kwargs)
            self.fields['title'].label = "作品主題"
            self.fields['file'].label = "作品檔案"
            self.fields['body'].label = "作品說明"
            self.fields['site'].label = "作品網址"
            self.fields['youtube'].label = "Youtube網址"
            self.fields['file'].required = False
            self.fields['site'].required = False
            self.fields['youtube'].required = False

# Python作品
class ShowForm2(forms.ModelForm):
        screenshot = forms.CharField(widget=forms.HiddenInput())

        class Meta:
           model = ShowGroup
           fields = ['code','title','body', 'youtube']

        def __init__(self, *args, **kwargs):
            super(ShowForm2, self).__init__(*args, **kwargs)
            self.fields['title'].label = "作品主題"
            self.fields['code'].label = "程式碼"
            self.fields['body'].label = "作品說明"
            self.fields['youtube'].label = "Youtube網址"
            self.fields['youtube'].required = False


# 評分
class ReviewForm1(forms.ModelForm):
        class Meta:
            model = ShowReview
            fields = ['score1', 'score2', 'score3', 'comment']

        #def __init__(self, *args, **kwargs):
            #super(ReviewForm, self).__init__(*args, **kwargs)
            #self.fields['score1'].label = "美工設計"
            #self.fields['score2'].label = "程式難度"
            #self.fields['score3'].label = "創意表現"
            #self.fields['comment'].label = "評語"

# 評分
class ReviewForm2(forms.ModelForm):
        class Meta:
            model = ShowReview
            fields = ['score', 'comment']


# 組別人數
class GroupShowSizeForm(forms.ModelForm):
        class Meta:
           model = Classroom
           fields = ['group_show_size']

        def __init__(self, *args, **kwargs):
            super(GroupShowSizeForm, self).__init__(*args, **kwargs)
            self.fields['group_show_size'].label = "小組人數"
