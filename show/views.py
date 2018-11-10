# -*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render
from show.models import ShowGroup, ShowReview, Round, ShowFile
from django.core.exceptions import ObjectDoesNotExist
from student.models import Enroll
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from show.forms import GroupForm, ShowForm1, ShowForm2, ReviewForm1, ReviewForm2, GroupShowSizeForm
from teacher.models import Classroom
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Sum
from account.models import Profile, PointHistory
from django.contrib.auth.models import User
from account.avatar import *
from django.core.exceptions import ObjectDoesNotExist
from collections import OrderedDict
from django.http import JsonResponse
from django.http import HttpResponse
import math
import cStringIO as StringIO
from PIL import Image,ImageDraw,ImageFont
from binascii import a2b_base64
import os
import StringIO
import zipfile
import xlsxwriter
from datetime import datetime
from django.utils.timezone import localtime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from wsgiref.util import FileWrapper
from operator import itemgetter
from django.views import generic
import json
from decimal import Decimal

def is_teacher(user, classroom_id):
    return user.groups.filter(name='teacher').exists() and Classroom.objects.filter(teacher_id=user.id, id=classroom_id).exists()

# 所有組別
def group(request, round_id):
        round = Round.objects.get(id=round_id)
        classroom_id = round.classroom_id
        classroom = Classroom.objects.get(id=classroom_id)   
        student_groups = []
        group_show_open = Classroom.objects.get(id=classroom_id).group_show_open
        shows = ShowGroup.objects.filter(round_id=round_id)
        show_ids = map(lambda a: a.id, shows)
        nogroup = list(Enroll.objects.filter(classroom_id=classroom_id))
        try:
                group_show = Enroll.objects.get(student_id=request.user.id, classroom_id=classroom_id).groupshow
                if group_show:
                    student_group = map(int, group_show.split(","))
                else :
                    student_group = []
        except ObjectDoesNotExist :
                student_group = []		
        for show in shows:
            enrolls = Enroll.objects.filter(classroom_id=classroom_id, groupshow__icontains=show.id)
            for enroll in enrolls:
                nogroup.remove(enroll)
            student_groups.append([show, enrolls,  classroom.group_show_size-len(enrolls)])
            
        #找出尚未分組的學生
        def getKey(custom):
            return custom.seat	
        nogroup = sorted(nogroup, key=getKey)             
        return render(request, 'show/group.html', {'shows':shows, 'round_id':round_id, 'nogroup': nogroup, 'group_show_open':group_show_open, 'teacher':is_teacher(request.user, classroom_id), 'student_groups':student_groups, 'classroom_id':classroom_id, 'student_group':student_group})

# 新增組別
def group_add(request, round_id):
        show = Round.objects.get(id=round_id)
        classroom_id = show.classroom_id
        classroom_name = Classroom.objects.get(id=classroom_id).name
        if request.method == 'POST':
            form = GroupForm(request.POST)
            if form.is_valid():
                group = ShowGroup(name=form.cleaned_data['name'],round_id=int(round_id))
                group.save()
                enrolls = Enroll.objects.filter(classroom_id=classroom_id)
                for enroll in enrolls :
                    review = ShowReview(show_id=group.id, student_id=enroll.student_id)
                    review.save()
                return redirect('/show/group/'+round_id)
        else:
            form = GroupForm()
        return render(request, 'show/group_add.html', {'form':form})

# 新增創意秀
def round_add(request, classroom_id):
        round = Round(classroom_id=classroom_id)
        round.save()                  
        return redirect('/show/group/'+str(round.id))
			
# 設定組別人數
def group_size(request, round_id):
        show = Round.objects.get(id=round_id)
        classroom_id = show.classroom_id	
        if request.method == 'POST':
            form = GroupShowSizeForm(request.POST)
            if form.is_valid():
                classroom = Classroom.objects.get(id=classroom_id)
                classroom.group_show_size = form.cleaned_data['group_show_size']
                classroom.save()

                return redirect('/show/group/'+str(round_id))
        else:
            classroom = Classroom.objects.get(id=classroom_id)
            form = GroupShowSizeForm(instance=classroom)
        return render(request, 'show/group_size.html', {'form':form})        

# 加入組別
def group_enroll(request, round_id,  group_id):
        round = Round.objects.get(id=round_id)
        classroom_id = round.classroom_id	
        classroom_name = Classroom.objects.get(id=classroom_id).name    
        group_name = ShowGroup.objects.get(id=group_id).name
        enrolls = Enroll.objects.filter(student_id=request.user.id, classroom_id=classroom_id)
        if len(enrolls)>0:
          if enrolls[0].groupshow:
            groups = map(int, enrolls[0].groupshow.split(","))
          else:
            groups = []
          shows = ShowGroup.objects.filter(round_id=round_id)
          for show in shows:
            if show.id in groups:
              groups.remove(show.id)
          groups.append(int(group_id))
          enrolls.update(groupshow=str(groups).replace("[", "").replace("]", ""))
                  
        return redirect('/show/group/'+round_id)

# 刪除組別
def group_delete(request, group_id, round_id):
        round = Round.objects.get(id=round_id)
        classroom_name = Classroom.objects.get(id=round.classroom_id).name    
        group_name = ShowGroup(id=group_id).name    
        group = ShowGroup.objects.get(id=group_id)
  
        group.delete()
        return redirect('/show/group/'+round_id)    

# 開放選組
def group_open(request, round_id, action):
    show = Round.objects.get(id=round_id)
    classroom_id = show.classroom_id	
    classroom = Classroom.objects.get(id=classroom_id)
    if action == "1":
        classroom.group_show_open=True
        classroom.save()
  
    else :
        classroom.group_show_open=False
        classroom.save()
          
    return redirect('/show/group/'+round_id)  	
	
# 創意秀清單
class ShowListView(generic.ListView):
    model = Round
    template_name = 'show/round_list.html'
    
    def get_queryset(self):
        shows = Round.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")      
        return shows
      
    def get_context_data(self, **kwargs):
        context = super(ShowListView, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        return context    
  
# 上傳創意秀
class ShowUpdateView(UpdateView):
  
    def get_form_class(self):
        classroom_id = Round.objects.get(id=self.kwargs['round_id']).classroom_id
        classroom = Classroom.objects.get(id=classroom_id)
        if classroom.lesson == 1:
            return ShowForm1
        else :
            return ShowForm2

    def get(self, request, **kwargs):
        self.object = ShowGroup.objects.get(id=self.kwargs['group_show'])
        members = Enroll.objects.filter(groupshow__icontains=self.kwargs['group_show'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form, members=members, show_id=self.object.id)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = ShowGroup.objects.get(id=self.kwargs['group_show'])
        return obj
		
    def form_valid(self, form):
        classroom_id = Round.objects.get(id=self.kwargs['round_id']).classroom_id
        classroom = Classroom.objects.get(id=classroom_id)
        obj = form.save(commit=False)
        showfiles = []
        try:
            filepath = self.request.FILES['file']
        except :
            filepath = False
          
        # 限制小組成員才能上傳
        pmembers = Enroll.objects.filter(groupshow__icontains=self.kwargs['show_id'])
        members = []
        for member in pmembers:
            groups = member.groupshow.split(",")
            if self.kwargs['show_id'] in groups:
                members.append(member)		
        is_member = False
        for member in members :
            if self.request.user.id == member.student_id:
                is_member = True
        
        if is_member : 
            if classroom.lesson == 1 and filepath :
                myfile = self.request.FILES['file']
                fs = FileSystemStorage(settings.BASE_DIR+"/static/show/"+self.kwargs['group_show']+"/")
                filename = uuid4().hex+".sb2"
                fs.save(filename, myfile)
                obj.file = filename	
            #save object
            start = obj.youtube.find("v=")
            if start > 0:
                obj.youtube = obj.youtube[start+2:start+13]
            obj.publish = timezone.now()
            obj.done = True
            obj.save()
            
            if not classroom.lesson == 1:
                dataURI = form.cleaned_data['screenshot']
                try:
                    head, data = dataURI.split(',', 1)
                    mime, b64 = head.split(';', 1)
                    mtype, fext = mime.split('/', 1)
                    binary_data = a2b_base64(data)

                    prefix = 'static/show/pic/'
                    directory = "{prefix}/".format(prefix=prefix)
                    image_file = "{path}/{id}.jpg".format(path=directory, id=obj.id)

                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    with open(image_file, 'wb') as fd:
                        fd.write(binary_data)
                        fd.close()
                    obj.picture=image_file
                except ValueError:
                    path = dataURI.split('/')
                    obj.picture=path[0]
                obj.save()
            
							
								
            if obj.done == False:
                for member in members:			
			        # credit
                    update_avatar(member.student_id, 4, 3)
                    # History
                    history = PointHistory(user_id=member.student_id, kind=4, message=u'3分--繳交創意秀<'+obj.title+'>', url='/show/detail/'+str(obj.id))
                    history.save()

            return redirect('/show/group/'+self.kwargs['round_id'])
        else :
            return redirect('/')

# 評分
class ReviewUpdateView(UpdateView):
    model = ShowReview
    template_name_suffix = '_review'
    
    def get_form_class(self):
        classroom_id = Round.objects.get(id=self.kwargs['round_id']).classroom_id
        classroom = Classroom.objects.get(id=classroom_id)
        if classroom.lesson == 1:
            return ReviewForm1
        else :
            return ReviewForm2    

    def get(self, request, **kwargs):
        show = ShowGroup.objects.get(id=self.kwargs['show_id'])
        try:
            self.object = ShowReview.objects.get(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
        except ObjectDoesNotExist:
            self.object = ShowReview(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
            self.object.save()        
        reviews = ShowReview.objects.filter(show_id=self.kwargs['show_id'], done=True)
        score0 = reviews.aggregate(Sum('score')).values()[0]
        score1 = reviews.aggregate(Sum('score1')).values()[0]
        score2 = reviews.aggregate(Sum('score2')).values()[0]
        score3 = reviews.aggregate(Sum('score3')).values()[0]
        score = [self.object.score1, self.object.score2,self.object.score3]
        if reviews.count() > 0 :
            score0 = score0 / reviews.count()     
            score1 = score1 / reviews.count()     
            score2 = score2 / reviews.count()  
            score3 = score3 / reviews.count()
            def show_category(show_id):
                show = ShowGroup.objects.get(id=show_id)
                round = Round.objects.get(id=show.round_id)
                classroom = Classroom.objects.get(id=round.classroom_id)
                if classroom.lesson == 1:
                    return 1
                else :
                    return 2
            if show_category(self.kwargs['show_id']) == 1:
                scores = [math.ceil(score1*10)/10, math.ceil(score2*10)/10, math.ceil(score3*10)/10,  reviews.count()]
            else :
                scores = [math.ceil(score0*10)/10, 0, 0, reviews.count()]
        else :
            scores = [0,0,0,0]
        pmembers = Enroll.objects.filter(groupshow__icontains=self.kwargs['show_id'])
        members = []
        for member in pmembers:
            groups = member.groupshow.split(",")
            if self.kwargs['show_id'] in groups:
                members.append(member)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        showfiles = ShowFile.objects.filter(show_id=self.kwargs['show_id']).order_by("-id")
        round = Round.objects.get(id=self.kwargs['round_id'])
        teacher = is_teacher(self.request.user, round.classroom_id)				
        context = self.get_context_data(groups=groups, teacher=teacher, showfiles=showfiles, show=show, form=form, members=members, review=self.object, scores=scores, score=score, reviews=reviews)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        try :
            obj = ShowReview.objects.get(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
        except ObjectDoesNotExist:
            obj = ShowReview(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
            obj.save()
        return obj
	
    def form_valid(self, form):
        show = ShowGroup.objects.get(id=self.kwargs['show_id'])        
        #save object
        obj = form.save(commit=False)
        if obj.done == False:
            round_id = ShowGroup.objects.get(id=self.kwargs['show_id']).round_id
            classroom_id = Round.objects.get(id=round_id).classroom_id
            member = Enroll.objects.get(classroom_id=classroom_id, student_id=self.request.user.id)
            # credit
            update_avatar(member.student_id, 4, 1)
            # History
            show = ShowGroup.objects.get(id=self.kwargs['show_id'])			
            history = PointHistory(user_id=member.student_id, kind=4, message=u'1分--評分創意秀<'+show.title+'>', url='/show/detail/'+str(show.id))
            history.save()
        obj.publish = timezone.now()
        obj.done = True
        obj.save()    
        classroom_id = Round.objects.get(id=self.kwargs['round_id']).classroom_id
        classroom = Classroom.objects.get(id=classroom_id)
        if classroom.lesson == 1:
            return redirect('/show/detail/'+self.kwargs['round_id']+'/'+self.kwargs['show_id'])
        else :
            return redirect('/show/detail/'+self.kwargs['round_id']+'/'+self.kwargs['show_id']) 


# 所有同學的評分		
class ReviewListView(ListView):
    context_object_name = 'reviews'
    template_name = 'show/reviewlist.html'
    def get_queryset(self):
        show = ShowGroup.objects.get(id=self.kwargs['show_id'])        
 
        return ShowReview.objects.filter(show_id=self.kwargs['show_id'], done=True).order_by("-publish")

    def get_context_data(self, **kwargs):
        ctx = super(ReviewListView, self).get_context_data(**kwargs)
        try :
           review = ShowReview.objects.get(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
        except ObjectDoesNotExist:
            review = ShowReview(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
            review.save()        
        show = ShowGroup.objects.get(id=self.kwargs['show_id']) 
        pmembers = Enroll.objects.filter(groupshow__icontains=self.kwargs['show_id'])
        members = []
        for member in pmembers:
            groups = member.groupshow.split(",")
            if self.kwargs['show_id'] in groups:
                members.append(member)
        reviews = ShowReview.objects.filter(show_id=self.kwargs['show_id'], done=True)
        score1 = reviews.aggregate(Sum('score1')).values()[0]
        score2 = reviews.aggregate(Sum('score2')).values()[0]
        score3 = reviews.aggregate(Sum('score3')).values()[0]
        score = [review.score1, review.score2, review.score3]
        if reviews.count() > 0 :
            score1 = score1 / reviews.count()     
            score2 = score2 / reviews.count()  
            score3 = score3 / reviews.count()          
            scores = [math.ceil(score1*10)/10, math.ceil(score2*10)/10, math.ceil(score3*10)/10,  score1+score2+score3, reviews.count()]
        else :
            scores = [0,0,0,0]        
        ctx['scores'] = scores
        ctx['show'] = show
        ctx['members'] = members
        round = Round.objects.get(id=show.round_id)
        ctx['teacher'] = is_teacher(self.request.user, round.classroom_id)
        return ctx

# 排行榜
class RankListView(ListView):
    context_object_name = 'lists'
    template_name = 'show/ranklist.html'
    def get_queryset(self):
        def getKey(custom):
            return custom[2]	
        lists = []
        show = Round.objects.get(id=self.kwargs['round_id'])
        classroom_id = show.classroom_id				
        shows = ShowGroup.objects.filter(round_id=self.kwargs['round_id'])
        for show in shows :
            pmembers = Enroll.objects.filter(groupshow__icontains=str(show.id))
            students = []
            for member in pmembers:
                groups = member.groupshow.split(",")
                if self.kwargs['show_id'] in groups:
                    students.append(member)
            reviews = ShowReview.objects.filter(show_id=show.id, done=True)	
            if reviews.count() > 0 :			
                score = reviews.aggregate(Sum('score'+self.kwargs['rank_id'])).values()[0]/reviews.count()
            else :
                score = 0
            lists.append([show, students, score, reviews.count(), self.kwargs['rank_id'], self.kwargs['round_id']])
            lists= sorted(lists, key=getKey, reverse=True)

        return lists

def show_download(request, show_id, showfile_id):
    showfile = ShowFile.objects.get(id=showfile_id)
    show = ShowGroup.objects.get(id=show_id)
    pmembers = Enroll.objects.filter(groupshow__icontains=show_id)
    members = []
    for member in pmembers:
        groups = member.groupshow.split(",")
        if str(show_id) in groups:
            members.append(member)
    username = ""
    for member in members:
        username = username + member.student.first_name + "_"
    filename = show_id + "_" + username + "_" + show.title + ".sb2"
    download =  settings.BASE_DIR + "/" + showfile.filename
    wrapper = FileWrapper(file( download, "r" ))
    response = HttpResponse(wrapper, content_type = 'application/force-download')
    #response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename.encode('utf8'))
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
    #return render(request, 'student/download.html', {'download':download})
			
# 教師查看創意秀評分情況
class TeacherListView(ListView):
    context_object_name = 'lists'
    template_name = 'show/teacherlist.html'
			
    def get_context_data(self, **kwargs):
        context = super(TeacherListView, self).get_context_data(**kwargs)
        context['round_id'] = self.kwargs['round_id']
        return context

    def get_queryset(self):
        lists = {}
        counter = 0
        round = Round.objects.get(id=self.kwargs['round_id'])
        classroom_id = round.classroom_id								
        enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by('seat')
        classroom_name = Classroom.objects.get(id=classroom_id).name
        for enroll in enrolls:
            lists[enroll.id] = []	            
            shows = ShowGroup.objects.filter(round_id=round.id).order_by("-id")
            if not shows.exists():
                lists[enroll.id].append([enroll])
            else :
                counter = 0
                for show in shows:
                    pmembers = Enroll.objects.filter(groupshow__icontains=str(show.id))
                    members = []
                    for member in pmembers:
                        groups = member.groupshow.split(",")
                        if str(show.id) in groups:
                            members.append(member)
                    try: 
                        review = ShowReview.objects.get(show_id=show.id, student_id=enroll.student_id)
                    except ObjectDoesNotExist:
                        review = ShowReview(show_id=show.id)
                    if review.done:
                        counter += 1
                    lists[enroll.id].append([enroll, review, show, members, counter])
        lists = OrderedDict(sorted(lists.items(), key=lambda x: x[1][0][0].seat))
        return lists
        
# 教師查看創意秀評分情況
class ScoreListView(ListView):
    context_object_name = 'lists'
    template_name = 'show/scorelist.html'
    def get_queryset(self):
        lists = {}
        counter = 0
        show = Round.objects.get(id=self.kwargs['round_id'])
        classroom_id = show.classroom_id								
        enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by('seat')
        classroom_name = Classroom.objects.get(id=classroom_id).name
        shows = ShowGroup.objects.filter(round_id=show.id)
        for showa in shows:
            pmembers = Enroll.objects.filter(groupshow__icontains=str(showa.id))
            members = []
            for member in pmembers:
                groups = member.groupshow.split(",")
                if str(showa.id) in groups:
                    members.append(member)
            reviews = ShowReview.objects.filter(show_id=showa.id, done=True)
            score1 = reviews.aggregate(Sum('score1')).values()[0]
            score2 = reviews.aggregate(Sum('score2')).values()[0]
            score3 = reviews.aggregate(Sum('score3')).values()[0]
            if reviews.count() > 0 :
                score1 = score1 / reviews.count()     
                score2 = score2 / reviews.count()  
                score3 = score3 / reviews.count()          
                scores = [math.ceil(score1*10)/10, math.ceil(score2*10)/10, math.ceil(score3*10)/10,  score1+score2+score3, reviews.count()]
            else :
                scores = [0,0,0,0]        
            lists[showa.id] = [showa, scores, members, self.kwargs['round_id']]
 
        lists = OrderedDict(sorted(lists.items(), key=lambda x: x[1][1][3], reverse=True))
        #lists = OrderedDict(sorted(lists.items(), key=itemgetter(1)))
        return lists

# 藝廊                  
class GalleryListView(ListView):
    context_object_name = 'lists'
    paginate_by = 10
    template_name = 'show/gallerylist.html'
    def get_queryset(self):
        # Scratch創意秀
        if self.kwargs['category'] == "1":
            classroom_pool = [classroom for classroom in Classroom.objects.filter(lesson=1)]
        # VPhysics創意秀
        else:
            classroom_pool = [classroom for classroom in Classroom.objects.filter(lesson__in=[2,4])]
        classroom_ids = map(lambda a: a.id, classroom_pool)
        round_pool = [round for round in Round.objects.filter(classroom_id__in=classroom_ids)]
        round_ids = map(lambda a: a.id, round_pool)           
        return ShowGroup.objects.filter(gallery=True, round_id__in=round_ids).order_by('-publish')
      
    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        return context         
		
# 查看藝郎某項目
def GalleryDetail(request, show_id):
    show = ShowGroup.objects.get(id=show_id)
    reviews = ShowReview.objects.filter(show_id=show_id, done=True)
    score1 = reviews.aggregate(Sum('score1')).values()[0]
    score2 = reviews.aggregate(Sum('score2')).values()[0]
    score3 = reviews.aggregate(Sum('score3')).values()[0]
    if reviews.count() > 0 :
        score1 = score1 / reviews.count()     
        score2 = score2 / reviews.count()  
        score3 = score3 / reviews.count()          
        scores = [math.ceil(score1*10)/10, math.ceil(score2*10)/10, math.ceil(score3*10)/10,  reviews.count()]
    else :
        scores = [0,0,0,0]        
    pmembers = Enroll.objects.filter(groupshow__icontains=str(show_id))
    members = []
    for member in pmembers:
        groups = member.groupshow.split(",")
        if str(show_id) in groups:
            members.append(member)

    classroom_id = Round.objects.get(id=show.round_id).classroom_id
    showfiles = ShowFile.objects.filter(show_id=show.id)
    
    return render(request, 'show/gallerydetail.html', {'show': show, 'showfiles':showfiles, 'members':members, 'scores':scores, 'reviews':reviews, 'teacher':is_teacher(request.user, classroom_id)})

# 將創意秀開放到藝廊
def make(request):
    show_id = request.POST.get('showid')
    action = request.POST.get('action')
    if show_id and action :
        show = ShowGroup.objects.get(id=show_id)	      
        try :
            show = ShowGroup.objects.get(id=show_id)	
            if action == 'open':
                show.gallery = True             
            else:
                show.gallery = False		
                     
            show.save()
        except ObjectDoesNotExist :
            pass
        return JsonResponse({'status':'ok'}, safe=False)        
    else:
        return JsonResponse({'status':'ko'}, safe=False)       
        
def excel(request, round_id):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)    
            
    shows = ShowGroup.objects.filter(round_id=round_id)
    
    worksheet = workbook.add_worksheet(u"分組")
    c = 0
    for show in shows:
        worksheet.write(c, 0, show.name)
        worksheet.write(c, 1, show.title)
        #worksheet.write(c, 2, "https://scratch.mit.edu/projects/"+show.number)
        number = 3
        members = Enroll.objects.filter(groupshow__icontains=str(show.id)+",")
        for member in members:
            worksheet.write(c, number, "("+str(member.seat)+")"+member.student.first_name)
            number = number + 1        
        c = c + 1
    for show in shows :
        worksheet = workbook.add_worksheet(show.name)
        worksheet.write(0,0, u"組員")
        number = 1
        members = Enroll.objects.filter(groupshow__icontains=str(show.id)+",")
        for member in members:
            worksheet.write(0, number, "("+str(member.seat)+")"+member.student.first_name)
            number = number + 1
        worksheet.write(1,0, u"作品名稱") 
        worksheet.write(1,1, show.title)
        worksheet.write(2,0, u"上傳時間") 
        worksheet.write(2,1, str(localtime(show.publish)))        
        #worksheet.write(3,1, "https://scratch.mit.edu/projects/"+str(show.number))

        worksheet.write(3,0, u"評分者")
        worksheet.write(3,1, u"美工設計")
        worksheet.write(3,2, u"程式難度")
        worksheet.write(3,3, u"創意表現")
        worksheet.write(3,4, u"評語")
        worksheet.write(3,5, u"時間")
        showreviews = ShowReview.objects.filter(show_id=show.id)        
        score1 = showreviews.aggregate(Sum('score1')).values()[0]
        score2 = showreviews.aggregate(Sum('score2')).values()[0]
        score3 = showreviews.aggregate(Sum('score3')).values()[0]
        if showreviews.count() > 0 :
            score1 = score1 / showreviews.count()     
            score2 = score2 / showreviews.count()  
            score3 = score3 / showreviews.count()          
            scores = [math.ceil(score1*10)/10, math.ceil(score2*10)/10, math.ceil(score3*10)/10,  showreviews.count()]
        else :
            scores = [0,0,0,0]
        
        worksheet.write(4,0, u"平均("+str(scores[3])+u"人)")
        worksheet.write(4,1, scores[0])
        worksheet.write(4,2, scores[1])
        worksheet.write(4,3, scores[2])        

        index = 5
        
        reviews = []
        classroom_id = Round.objects.get(id=round_id).classroom_id
        for showreview in showreviews:
            enroll = Enroll.objects.get(classroom_id=classroom_id, student_id=showreview.student_id)
            reviews.append([showreview, enroll])
        
        def getKey(custom):
            return custom[1].seat
	
        reviews = sorted(reviews, key=getKey)        
        for review in reviews:
            worksheet.write(index,0, "("+str(review[1].seat)+")"+review[1].student.first_name)
            worksheet.write(index,1, review[0].score1)
            worksheet.write(index,2, review[0].score2)
            worksheet.write(index,3, review[0].score3)            
            worksheet.write(index,4, review[0].comment)  
            worksheet.write(index,5, str(localtime(review[0].publish)))             
            index = index + 1
        worksheet.insert_image(index+1,0, 'static/show/'+str(show.id)+'/Dr-Scratch.png')
    workbook.close()
    # xlsx_data contains the Excel file
    #response = HttpResponse(content_type='application/vnd.ms-excel')
    #response['Content-Disposition'] = 'attachment; filename=Show'+str(datetime.now().date())+'.xlsx'
    xlsx_data = output.getvalue()
    #response.write(xlsx_data)
    xls_file = "static/show/content.xlsx"
    directory = 'static/show/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(xls_file, 'wb') as fd:
        fd.write(xlsx_data)
        fd.close()
    #return output

def classroom(request, classroom_id):
    rounds = Round.objects.filter(classroom_id=classroom_id)
    classroom = Classroom.objects.get(id=classroom_id)
    return render(request, 'show/classroom.html', {'classroom':classroom, 'rounds': rounds})

def commentall(request, round_id):
    round = Round.objects.get(id=round_id)
    classroom = Classroom.objects.get(id=round.classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=round.classroom_id)
    return render(request, 'show/commentall.html', {'classroom':classroom, 'round':round, 'enrolls': enrolls})

def comment(request, round_id, user_id):
    classroom_id = Round.objects.get(id=round_id).classroom_id
    classroom = Classroom.objects.get(id=classroom_id)
    reviews = ShowReview.objects.filter(student_id=user_id)
    user = User.objects.get(id=user_id)
    lists = []
    for review in reviews:
        shows = ShowGroup.objects.filter(id=review.show_id)
        for show in shows:
            if review.comment != "":
                lists.append([show, review, round_id])
    return render(request, 'show/comment.html', {'user':user, 'classroom':classroom, 'lists': lists})

def zip(request, round_id):
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    #filenames = [settings.BASE_DIR + "/static/certificate/sample1.jpg", settings.BASE_DIR + "/static/certificate/sample2.jpg"]
    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    round = Round.objects.get(id=round_id)
    classroom = Classroom.objects.get(id=round.classroom_id)
    zip_subdir = u"創意秀_" + classroom.name + u"班_" + round_id
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    excelfile = excel(request, round_id)
    filename = "content.xlsx"
    zip_path = os.path.join(zip_subdir, filename)
    fdir = settings.BASE_DIR + "/static/show/"
    fname = "content.xlsx"
    fpath = fdir + fname    	
    zf.write(fpath, zip_path)

    shows = ShowGroup.objects.filter(round_id=round_id)
    for show in shows:
        try:
          showfiles = ShowFile.objects.filter(show_id=show.id).order_by("-id")
          # Calculate path for file in zip
          #fdir , fname = os.path.split(fpath)
          if showfiles.exists():
            fdir = settings.BASE_DIR + "/"
            fname = showfiles[0].filename
            fpath = fdir + fname
            enrolls = Enroll.objects.filter(groupshow__icontains=str(show.id)+",")
            members = ""
            for enroll in enrolls:
                members += enroll.student.first_name+"_"
            filename = show.name + "_" + members + show.title + ".sb2"
            zip_path = os.path.join(zip_subdir, filename)

            # Add file, at correct path
            zf.write(fpath, zip_path)
        except ObjectDoesNotExist:
            pass

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename={0}'.format(zip_filename.encode('utf8'))

    return resp