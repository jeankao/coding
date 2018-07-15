# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from teacher.models import Classroom, ImportUser, TWork
from student.models import Enroll, EnrollGroup, Work, WorkAssistant, WorkFile
from account.models import Message, MessagePoll, MessageContent, PointHistory
from account.avatar import *
from .forms import ClassroomForm, AnnounceForm, ScoreForm, UploadFileForm, CheckForm, CheckForm1, CheckForm2, CheckForm3, CheckForm4, CheckForm_vphysics, CheckForm_euler
from .forms import WorkForm
from django.contrib.auth.decorators import login_required
from student.lesson import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper
from collections import OrderedDict
import django_excel as excel
from account.forms import PasswordForm, RealnameForm
import sys
from uuid import uuid4
import os

reload(sys)

sys.setdefaultencoding('utf-8')

# 判斷是否為授課教師
def is_teacher(user, classroom_id):
    return user.groups.filter(name='teacher').exists() and Classroom.objects.filter(teacher_id=user.id, id=classroom_id).exists()

def not_in_teacher_group(user):
    if not user.groups.filter(name='teacher').exists():
        return False
    return True

# 列出所有課程
class ClassroomListView(ListView):
    model = Classroom
    context_object_name = 'classrooms'
    paginate_by = 50
    def dispatch(self, *args, **kwargs):
        if not not_in_teacher_group(self.request.user):
            raise PermissionDenied
        else :
            return super(ClassroomListView, self).dispatch(*args, **kwargs)
    def get_queryset(self):
        queryset = Classroom.objects.filter(teacher_id=self.request.user.id).order_by("-id")
        return queryset

#新增一個課程
class ClassroomCreateView(CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'form.html'
    def dispatch(self, *args, **kwargs):
        if not not_in_teacher_group(self.request.user):
            raise PermissionDenied
        else :
            return super(ClassroomCreateView, self).dispatch(*args, **kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.teacher_id = self.request.user.id
        self.object.save()
        # 將教師設為0號學生
        enroll = Enroll(classroom_id=self.object.id, student_id=self.request.user.id, seat=0)
        enroll.save()

        return redirect("/teacher/classroom")

# 修改選課密碼
@login_required
@user_passes_test(not_in_teacher_group, login_url='/')
def classroom_edit(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom.name =form.cleaned_data['name']
            classroom.password = form.cleaned_data['password']
            classroom.save()
            return redirect('/teacher/classroom')
    else:
        form = ClassroomForm(instance=classroom)

    return render_to_response('teacher/classroom_form.html',{'form': form}, context_instance=RequestContext(request))

# 退選
@login_required
@user_passes_test(not_in_teacher_group, login_url='/')
def unenroll(request, enroll_id, classroom_id):
    enroll = Enroll.objects.get(id=enroll_id)
    enroll.delete()
    classroom_name = Classroom.objects.get(id=classroom_id).name

    return redirect('/student/classmate/'+classroom_id)

# 設定班級助教
@login_required
@user_passes_test(not_in_teacher_group, login_url='/')
def classroom_assistant(request, classroom_id):
    assistants = Assistant.objects.filter(classroom_id=classroom_id).order_by("-id")
    classroom = Classroom.objects.get(id=classroom_id)

    return render_to_response('teacher/assistant.html',{'assistants': assistants, 'classroom':classroom}, context_instance=RequestContext(request))

# 教師可以查看所有帳號
class AssistantListView(ListView):
    context_object_name = 'users'
    paginate_by = 20
    template_name = 'teacher/assistant_user.html'
    def dispatch(self, *args, **kwargs):
        if not not_in_teacher_group(self.request.user):
            raise PermissionDenied
        else :
            return super(AssistantListView, self).dispatch(*args, **kwargs)
    def get_queryset(self):
        if self.request.GET.get('account') != None:
            keyword = self.request.GET.get('account')
            queryset = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword)).order_by('-id')
        else :
            queryset = User.objects.all().order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AssistantListView, self).get_context_data(**kwargs)
        context['classroom'] = Classroom.objects.get(id=self.kwargs['classroom_id'])
        assistant_list = []
        assistants = Assistant.objects.filter(classroom_id=self.kwargs['classroom_id'])
        for assistant in assistants:
            assistant_list.append(assistant.user_id)
        context['assistants'] = assistant_list
        return context

# 列出所有助教課程
class AssistantClassroomListView(ListView):
    model = Classroom
    context_object_name = 'classrooms'
    template_name = 'teacher/assistant_list.html'
    paginate_by = 20
    def dispatch(self, *args, **kwargs):
        if not not_in_teacher_group(self.request.user):
            raise PermissionDenied
        else :
            return super(AssistantClassroomListView, self).dispatch(*args, **kwargs)
    def get_queryset(self):
        assistants = Assistant.objects.filter(user_id=self.request.user.id)
        classroom_list = []
        for assistant in assistants:
            classroom_list.append(assistant.classroom_id)
        queryset = Classroom.objects.filter(id__in=classroom_list).order_by("-id")
        return queryset

# Ajax 設為助教、取消助教
def assistant_make(request):
    classroom_id = request.POST.get('classroomid')
    user_id = request.POST.get('userid')
    action = request.POST.get('action')
    if user_id and action :
        if action == 'set':
            try :
                assistant = Assistant.objects.get(classroom_id=classroom_id, user_id=user_id) 
            except ObjectDoesNotExist :
                assistant = Assistant(classroom_id=classroom_id, user_id=user_id)
                assistant.save()
            # 將教師設為0號學生
            enroll = Enroll(classroom_id=classroom_id, student_id=user_id, seat=0)
            enroll.save()
        else :
            try :
                assistant = Assistant.objects.get(classroom_id=classroom_id, user_id=user_id)
                assistant.delete()
                enroll = Enroll.objects.filter(classroom_id=classroom_id, student_id=user_id)
                enroll.delete()
            except ObjectDoesNotExist :
                pass
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)

# 退選
@login_required
@user_passes_test(not_in_teacher_group, login_url='/')
def unenroll(request, enroll_id, classroom_id):
    enroll = Enroll.objects.get(id=enroll_id)
    enroll.delete()
    classroom_name = Classroom.objects.get(id=classroom_id).name
    return redirect('/student/classmate/'+classroom_id)

# 列出所有公告
class AnnounceListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'teacher/announce_list.html'
    paginate_by = 20
    def dispatch(self, *args, **kwargs):
        if not not_in_teacher_group(self.request.user):
            raise PermissionDenied
        else :
            return super(AnnounceListView, self).dispatch(*args, **kwargs)
    def get_queryset(self):
        queryset = Message.objects.filter(classroom_id=self.kwargs['classroom_id'], author_id=self.request.user.id).order_by("-id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AnnounceListView, self).get_context_data(**kwargs)
        context['classroom'] = Classroom.objects.get(id=self.kwargs['classroom_id'])
        return context

    # 限本班任課教師
    def render_to_response(self, context):
        if not is_teacher(self.request.user, self.kwargs['classroom_id']):
            return redirect('/')
        return super(AnnounceListView, self).render_to_response(context)

#新增一個公告
class AnnounceCreateView(CreateView):
    model = Message
    form_class = AnnounceForm
    template_name = 'teacher/announce_form.html'
    def dispatch(self, *args, **kwargs):
        if not not_in_teacher_group(self.request.user):
            raise PermissionDenied
        else :
            return super(AnnounceCreateView, self).dispatch(*args, **kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.title = u"[公告]" + self.object.title
        self.object.author_id = self.request.user.id
        self.object.classroom_id = self.kwargs['classroom_id']
        self.object.type = 1
        self.object.save()
        self.object.url = "/teacher/announce/detail/" + str(self.object.id)
        self.object.save()
        
        #附件
        files = []
        if self.request.FILES.getlist('files'):
             for file in self.request.FILES.getlist('files'):
                fs = FileSystemStorage()
                filename = uuid4().hex							
                fs.save("static/attach/"+str(self.request.user.id)+"/"+filename, file)								
                files.append([filename, file.name])
        if files:
            for file, name in files:
                content = MessageContent()
                content.title = name
                content.message_id = self.object.id
                content.filename = str(self.request.user.id)+"/"+file
                content.save()        
        # 班級學生訊息
        enrolls = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id'])
        for enroll in enrolls:
            messagepoll = MessagePoll(message_id=self.object.id, reader_id=enroll.student_id, message_type=1)
            messagepoll.save()
        return redirect("/teacher/announce/"+self.kwargs['classroom_id'])

    def get_context_data(self, **kwargs):
        context = super(AnnounceCreateView, self).get_context_data(**kwargs)
        context['classroom'] = Classroom.objects.get(id=self.kwargs['classroom_id'])
        return context


# 公告
def announce_detail(request, message_id):
    message = Message.objects.get(id=message_id)
    files = MessageContent.objects.filter(message_id=message_id)
    classroom = Classroom.objects.get(id=message.classroom_id)

    announce_reads = []

    messagepolls = MessagePoll.objects.filter(message_id=message_id)
    for messagepoll in messagepolls:
        try:
            enroll = Enroll.objects.get(classroom_id=message.classroom_id, student_id=messagepoll.reader_id)
            announce_reads.append([enroll.seat, enroll.student.first_name, messagepoll])
        except ObjectDoesNotExist:
            pass

    def getKey(custom):
        return custom[0]
    announce_reads = sorted(announce_reads, key=getKey)
    return render_to_response('teacher/announce_detail.html', {'files':files,'message':message, 'classroom':classroom, 'announce_reads':announce_reads}, context_instance=RequestContext(request))

# 列出所有課程
class WorkListView(ListView):
    model = Work
    context_object_name = 'works'
    template_name = 'teacher/work_list.html'
    def dispatch(self, *args, **kwargs):
        if not not_in_teacher_group(self.request.user):
            raise PermissionDenied
        else :
            return super(WorkListView, self).dispatch(*args, **kwargs)
    def get_queryset(self):
        if self.kwargs['lesson'] == "1":
            queryset = lesson_list1
        elif self.kwargs['lesson'] == "2":
            queryset = lesson_list2
        elif self.kwargs['lesson'] == "3":
            queryset = lesson_list3
        elif self.kwargs['lesson'] == "4":
            queryset = lesson_list4      
        elif self.kwargs['lesson'] == "5":
            queryset = lesson_list2         
        else:
            queryset = lesson_list1
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WorkListView, self).get_context_data(**kwargs)
        context['classroom'] = Classroom.objects.get(id=self.kwargs['classroom_id'])
        context['lesson'] = self.kwargs['lesson']
        return context

# 教師評分
@login_required
@user_passes_test(not_in_teacher_group, login_url='/')
# 列出某作業所有同學名單
def work_class(request, typing, lesson, classroom_id, index):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    classroom = Classroom.objects.get(id=classroom_id)
    classmate_work = []
    scorer_name = ""
    for enroll in enrolls:
        try:
            work = Work.objects.get(user_id=enroll.student_id, index=index, lesson_id=lesson)
            if work.scorer > 0 :
                scorer = User.objects.get(id=work.scorer)
                scorer_name = scorer.first_name
            else :
                scorer_name = "1"
        except ObjectDoesNotExist:
            work = Work(index=index, user_id=0, lesson_id=lesson)
        except MultipleObjectsReturned:
            work = Work.objects.filter(user_id=enroll.student_id, index=index, lesson_id=lesson).last()
        try:
            group_name = EnrollGroup.objects.get(id=enroll.group).name
        except ObjectDoesNotExist:
            group_name = "沒有組別"
        assistant = WorkAssistant.objects.filter(typing=0, classroom_id=classroom_id, student_id=enroll.student_id, lesson_id=lesson, index=index)
        if assistant.exists():
            classmate_work.append([enroll,work,1, scorer_name, group_name])
        else :
            classmate_work.append([enroll,work,0, scorer_name, group_name])
    def getKey(custom):
        return custom[0].seat

    classmate_work = sorted(classmate_work, key=getKey)
    return render_to_response('teacher/work_class.html',{'typing':typing, 'classmate_work': classmate_work, 'classroom':classroom, 'index': index, 'lesson':lesson}, context_instance=RequestContext(request))

# (小)教師評分
def scoring(request, lesson, classroom_id, user_id, index, typing):
    teacher = is_teacher(User.objects.get(id=request.user.id), classroom_id)
    if not teacher:
        if not WorkAssistant.objects.filter(typing=typing, lesson_id=lesson, index=index, classroom_id=classroom_id, student_id=request.user.id).exists():
            return redirect("/")
    if typing == "0":
        if lesson == "1":
            lesson_name = lesson_list1[int(index)-1][2]
        elif lesson == "2":
            lesson_name = lesson_list2[int(index)-1][1]
        elif lesson == "3":
            lesson_name = lesson_list3[int(index)-1][1]
        elif lesson == "4":
            lesson_name = lesson_list4[int(index)-1][1]
        elif lesson == "5":
            lesson_name = lesson_list2[int(index)-1][1]            
        else:
            lesson_name = lesson_list1[int(index)-1][1]
    elif typing == "1":
        lesson_name = TWork.objects.get(id=index).title
    user = User.objects.get(id=user_id)
    enroll = Enroll.objects.get(classroom_id=classroom_id, student_id=user_id)
    workfiles = []
    try:
        assistant = WorkAssistant.objects.filter(typing=typing, classroom_id=classroom_id,lesson_id=lesson, index=index,student_id=request.user.id)
    except ObjectDoesNotExist:
        if not is_teacher(request.user, classroom_id):
            return render_to_response('message.html', {'message':"您沒有權限"}, context_instance=RequestContext(request))

    try:
        work3 = Work.objects.get(typing=typing, user_id=user_id, index=index, lesson_id=lesson)
        pic = work3.id
    except ObjectDoesNotExist:
        work3 = Work(typing=typing, index=index, user_id=user_id, lesson_id=lesson)
        pic = 0
    except MultipleObjectsReturned:
        works = Work.objects.filter(typing=typing, user_id=user_id, index=index, lesson_id=lesson).order_by("-id")
        work3 = works[0]
        pic = work3.id
        if int(lesson) > 1 :
            prefix = ['static/work/vphysics', 'static/work/euler', 'static/work/ck', 'static/work/vphysics2'][int(lesson) - 2]
            directory = "{prefix}/{uid}/{index}".format(prefix=prefix, uid=user_id, index=index)
            for work in works:
                image_file = "{path}/{id}.jpg".format(path=directory, id=work.id)        
                if os.path.exists(image_file):
                    pic = work.id
                    break

    if request.method == 'POST':
        form = ScoreForm(request.user, request.POST)
        if form.is_valid():
            works = Work.objects.filter(typing=typing, index=index, user_id=user_id, lesson_id=lesson)
            if works.exists():
                if works[0].score < 0 :
                        # 小老師
                        if not is_teacher(request.user, classroom_id):
                            # credit
                            update_avatar(request.user.id, 2, 1)
                            # History
                            history = PointHistory(user_id=request.user.id, kind=2, message=u'1分--小老師:<'+lesson_name.decode('utf8')+u'><'+enroll.student.first_name+u'>', url="/student/work/show/"+lesson+"/"+index)
                            history.save()

                        # credit
                        update_avatar(enroll.student_id, 1, 1)
                        # History                        
                        history = PointHistory(user_id=user_id, kind=1, message=u'1分--作業受評<'+lesson_name.decode('utf8')+u'><'+request.user.first_name+u'>', url="/student/work/show/"+lesson+"/"+index)                                               
                        history.save()		                        

                works.update(score=form.cleaned_data['score'])
                works.update(scorer=request.user.id)

            if is_teacher(request.user, classroom_id):
                if form.cleaned_data['assistant']:
                    try :
                        assistant = WorkAssistant.objects.get(typing=typing, student_id=user_id, classroom_id=classroom_id, index=index, lesson_id=lesson)
                    except ObjectDoesNotExist:
                        assistant = WorkAssistant(typing=typing, student_id=user_id, classroom_id=classroom_id, index=index, lesson_id=lesson)
                        assistant.save()

                    # create Message
                    title = u"<" + assistant.student.first_name+ u">擔任小老師<" + lesson_name.decode('utf8') + u">"
                    url = "/teacher/score_peer/" + lesson + "/" + index + "/" + classroom_id + "/" + str(enroll.group)
                    message = Message(title=title, url=url, time=timezone.now())
                    message.save()

                    group = Enroll.objects.get(classroom_id=classroom_id, student_id=assistant.student_id).group
                    if group > 0 :
                        enrolls = Enroll.objects.filter(group = group)
                        for enroll in enrolls:
                            # message for group member
                            messagepoll = MessagePoll(message_id = message.id,reader_id=enroll.student_id)
                            messagepoll.save()
                return redirect('/teacher/work/class/'+typing+ "/" + lesson+"/"+classroom_id+'/'+index)
            else:
                return redirect('/teacher/score_peer/'+typing+"/"+lesson+"/"+index+'/'+classroom_id+'/'+str(enroll.group))

    else:
        works = Work.objects.filter(typing=typing, index=index, user_id=user_id)
        if not works.exists():
            form = ScoreForm(user=request.user)
        else:
            form = ScoreForm(instance=works[0], user=request.user)
            workfiles = WorkFile.objects.filter(work_id=works[0].id).order_by("-id")
    return render_to_response('teacher/scoring.html', {'form': form,'work':work3, 'pic':pic, 'workfiles':workfiles, 'teacher':teacher, 'student':user, 'classroom_id':classroom_id, 'lesson':lesson, 'index':index}, context_instance=RequestContext(request))

# 小老師評分名單
def score_peer(request, typing, lesson, index, classroom_id, group):
    if typing == "0":
        if lesson == "1":
            queryset = lesson_list1
        elif lesson == "2":
            queryset = lesson_list2
        elif lesson == "3":
            queryset = lesson_list3
        else:
            queryset = lesson_list1
    elif typing == "1":
        queryset = TWork.objects.filter(classroom_id=classroom_id)
    try:
        assistant = WorkAssistant.objects.get(typing=typing, lesson_id=lesson, index=index, classroom_id=classroom_id, student_id=request.user.id)
    except ObjectDoesNotExist:
        if typing == "0":
            return redirect("/student/group/work/"+lesson+"/"+index+"/"+classroom_id)
        elif typing == "1":
            return redirect("/student/group/work2/"+lesson+"/"+index+"/"+classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=classroom_id, group=group)
    lessons = ""
    classmate_work = []
    for enroll in enrolls:
        if not enroll.student_id == request.user.id :
            scorer_name = ""
            try:
                work = Work.objects.get(typing=typing, user_id=enroll.student.id, index=index, lesson_id=lesson)
                if work.scorer > 0 :
                    scorer = User.objects.get(id=work.scorer)
                    scorer_name = scorer.first_name
            except ObjectDoesNotExist:
                work = Work(typing=typing, index=index, user_id=enroll.student.id, lesson_id=lesson)
            except MultipleObjectsReturned:
                work = Work.objects.filter(typing=typing, user_id=enroll.student.id, index=index, lesson_id=lesson).order_by("-id")[0]
            classmate_work.append([enroll.student,work,1, scorer_name])
        lessons = queryset[int(index)-1]
    return render_to_response('teacher/score_peer.html',{'enrolls':enrolls, 'classmate_work': classmate_work, 'classroom_id':classroom_id, 'lesson':lesson, 'index': index}, context_instance=RequestContext(request))

# 心得
def memo(request, lesson, classroom_id):
    # 限本班任課教師
    if not is_teacher(request.user, classroom_id):
        return redirect("/")
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    classroom_name = Classroom.objects.get(id=classroom_id).name
    return render_to_response('teacher/memo.html', {'lesson':lesson, 'enrolls':enrolls, 'classroom_name':classroom_name}, context_instance=RequestContext(request))

# 評分某同學某進度心得
@login_required
@user_passes_test(not_in_teacher_group, login_url='/')
def check(request, typing, lesson, unit, user_id, classroom_id):
    # 限本班任課教師
    if not is_teacher(request.user, classroom_id):
        return redirect("/")

    user_name = User.objects.get(id=user_id).first_name
    lesson_dict = {}
    works = Work.objects.filter(typing=typing, user_id=user_id, lesson_id=lesson)
    enroll = Enroll.objects.get(student_id=user_id, classroom_id=classroom_id)    
    if typing == "0":
        if lesson == "1":
            for index,assignment in enumerate(lesson_list1):
                lesson_dict[index] = [assignment]
        elif lesson == "2" :
            for index,assignment in enumerate(lesson_list2):
                lesson_dict[index] = [assignment]
        elif lesson == "3" :
            for index,assignment in enumerate(lesson_list3):
                lesson_dict[index] = [assignment]
        elif lesson == "4" :
            for index,assignment in enumerate(lesson_list4):
                lesson_dict[index] = [assignment]      
        elif lesson == "5" :
            for index,assignment in enumerate(lesson_list2):
                lesson_dict[index] = [assignment]                  
    else :
        assignments = TWork.objects.filter(classroom_id=classroom_id)
        for assignment in assignments:
            lesson_dict[assignment.id] = [assignment]

    for work in works:
        if typing == "0":
            index = work.index - 1
        else:
            index = work.index
        if index in lesson_dict:
            lesson_dict[index].append(work.score)
            lesson_dict[index].append(work.publication_date)
            if work.score > 0:
                score_name = User.objects.get(id=work.scorer).first_name
                lesson_dict[index].append(score_name)
            else :
                lesson_dict[index].append("尚未評分!")
            lesson_dict[index].append(work.memo)
    if request.method == 'POST':
      if typing == "0":
        if lesson == "1":
            if unit == "1":
                form = CheckForm1(request.POST)
            elif unit == "2":
                form = CheckForm2(request.POST)
            elif unit == "3":
                form = CheckForm3(request.POST)
            elif unit == "4":
                form = CheckForm4(request.POST)
        elif lesson == "2":
            form = CheckForm_vphysics(request.POST)
        elif lesson == "3":
            form = CheckForm_euler(request.POST)
        elif lesson == "4":
            form = CheckForm_vphysics(request.POST)    
        elif lesson == "5":
            form = CheckForm_vphysics(request.POST)            
      else:      
          form = CheckForm(request.POST)        
      
      if form.is_valid():
        if typing == "0":
          if lesson == "1":
              if unit == "1":
                  enroll.score_memo1=form.cleaned_data['score_memo1']
              elif unit == "2":
                  enroll.score_memo2=form.cleaned_data['score_memo2']
              elif unit == "3":
                  enroll.score_memo3=form.cleaned_data['score_memo3']
              elif unit == "4":
                  enroll.score_memo4=form.cleaned_data['score_memo4']
          elif lesson == "2" :
              enroll.score_memo_vphysics=form.cleaned_data['score_memo_vphysics']
          elif lesson == "3":
              enroll.score_memo_euler=form.cleaned_data['score_memo_euler']   
          elif lesson == "4" :
              enroll.score_memo_vphysics2=form.cleaned_data['score_memo_vphysics']
          elif lesson == "5" :
              enroll.score_memo_vphysics3=form.cleaned_data['score_memo_vphysics']              
          enroll.save()
          if form.cleaned_data['certificate']:
              return redirect('/certificate/'+lesson+'/'+unit+'/'+str(enroll.id)+'/certificate')
          else:
              return redirect('/teacher/memo/'+lesson+"/"+classroom_id)              
        else :
          enroll.score_memo = form.cleaned_data['score_memo'] 
          enroll.save()
          return redirect('/teacher/memo/'+lesson+"/"+classroom_id)          
    else:
      if typing == "0":  
        if lesson == "1":
            if unit == "1":
                form = CheckForm1(instance=enroll)
            elif unit == "2":
                form = CheckForm2(instance=enroll)
            elif unit == "3":
                form = CheckForm3(instance=enroll)
            elif unit == "4":
                form = CheckForm4(instance=enroll)
        elif lesson == "2" or lesson == "4" or lesson == "5":
            form = CheckForm_vphysics(instance=enroll)
        elif lesson == "3":
            form = CheckForm_euler(instance=enroll)       
        else :
            form =  CheckForm1(instance=enroll)
      else :
        form =  CheckForm(instance=enroll)

    return render_to_response('teacher/check.html', {'typing':typing, 'works':works, 'lesson': lesson, 'unit':unit, 'form':form, 'works':works, 'lesson_list':sorted(lesson_dict.items()), 'enroll': enroll, 'classroom_id':classroom_id}, context_instance=RequestContext(request))

@login_required
@user_passes_test(not_in_teacher_group, login_url='/')
def grade(request, typing, lesson, unit, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if not request.user.id == classroom.teacher_id:
        return redirect("/")
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by('seat')
    user_ids = [enroll.student_id for enroll in enrolls]
    work_pool = Work.objects.filter(typing=typing, user_id__in=user_ids, lesson_id=lesson).order_by('id')
    lesson_dict = {}
    data = []
    lesson_list = [lesson_list1, lesson_list2, lesson_list3, lesson_list4, lesson_list2][int(lesson)-1]
    for enroll in enrolls:
      enroll_score = []
      total = 0
      stu_works = filter(lambda w: w.user_id == enroll.student_id, work_pool)
      if typing == "0":
        if lesson == "1":
            if unit == "1":
                lesson_list = lesson_list[0:17]
            elif unit == "2":
                lesson_list = lesson_list[17:25]
            elif unit == "3":
                lesson_list = lesson_list[25:33]
            elif unit == "4":
                lesson_list = lesson_list[33:41]
            
      else :
        lesson_list = TWork.objects.filter(classroom_id=classroom_id)
      for index, assignment in enumerate(lesson_list):
            works = filter(lambda w: w.index == index+1, stu_works)
            works_count = len(works)
            if works_count == 0:
                enroll_score.append([0, index])
                total += 60
            else:
                work = works[-1]
                enroll_score.append([work.score, index])
                if work.score == -1:
                    if works_count == 1:
                        total += 80
                    else: # Multiple
                        total += 75
                else:
                    total += work.score

            if lesson == "1":
                memo = [enroll.score_memo1, enroll.score_memo2, enroll.score_memo3, enroll.score_memo4][int(unit)-1]
            elif lesson == "2":
                memo = enroll.score_memo_vphysics
            elif lesson == "3":
                memo = enroll.score_memo_euler
            elif lesson == "4":
                memo = enroll.score_memo_vphysics2
            elif lesson == "5":
                memo = enroll.score_memo_vphysics3            
            grade = int(total / len(lesson_list) * 0.6 + memo * 0.4)
      data.append([enroll, enroll_score, memo, grade])
    return render_to_response('teacher/grade.html', {'typing':typing, 'lesson':lesson, 'unit':unit, 'lesson_list':lesson_list, 'classroom':classroom, 'data':data}, context_instance=RequestContext(request))

# 列出分組所有作業
@login_required
@user_passes_test(not_in_teacher_group, login_url='/')
def work1(request, lesson, classroom_id):
    classroom_name = Classroom.objects.get(id=classroom_id).name
    lessons = []
    lesson_dict = {}
    groups = [group for group in EnrollGroup.objects.filter(classroom_id=classroom_id)]
    enroll_pool = [enroll for enroll in Enroll.objects.filter(classroom_id=classroom_id).order_by('seat')]
    student_ids = map(lambda a: a.student_id, enroll_pool)
    work_pool = Work.objects.filter(user_id__in=student_ids, lesson_id=lesson)
    user_pool = [user for user in User.objects.filter(id__in=work_pool.values('scorer'))]
    assistant_pool = [assistant for assistant in Assistant.objects.filter(classroom_id=classroom_id)]
    if lesson == "1":
        assignments = lesson_list
    else :
        assignments = TWork.objects.filter(classroom_id=classroom_id)
    for index,assignment in enumerate(assignments):
        works = []
        if lesson == "1":
            lesson_dict[index] = [assignment[1]]
        else:
            lesson_dict[index] = [assignment.title]
        student_groups = []
        for group in groups:
            members = filter(lambda u: u.group == group.id, enroll_pool)
            group_assistants = []
            scorer_name = ""
            for member in members:
                if lesson == "1":
                    sworks = filter(lambda w: w.index == index and w.student_id == member.student_id, work_pool)
                else:
                    sworks = filter(lambda w: w.index == assignment.id and w.student_id == enroll.student_id, work_pool)
                if sworks:
                    work = sworks[-1]
                    scorer = filter(lambda u: u.id == work.scorer, user_pool)
                    scorer_name = scorer[0].first_name if scorer else 'X'
                else:
                    work = SWork(index=index, student_id=1)
                works.append([member, work.score, scorer_name, work.memo])
                assistant = filter(lambda a: a.student_id == member.student_id and a.index == index, assistant_pool)
                if assistant:
                    group_assistants.append(member)
            student_groups.append([group, works, group_assistants])
        lessons.append([lesson_list[index], student_groups])
    return render_to_response('teacher/work1.html', {'lesson':lesson, 'lessons':lessons, 'classroom_id':classroom_id}, context_instance=RequestContext(request))

# Ajax 設為教師、取消教師
def make(request):
    classroom_id = request.POST.get('classroomid')
    user_id = request.POST.get('userid')
    action = request.POST.get('action')
    lesson = request.POST.get('lesson')
    index = request.POST.get('index')
    if lesson == "1":
        queryset = lesson_list1
        assignment = queryset[int(index)-1][2]
    elif lesson == "2":
        queryset = lesson_list2
        assignment = queryset[int(index)-1][1]
    elif lesson == "3":
        queryset = lesson_list3
        assignment = queryset[int(index)-1][1]
    else:
        queryset = lesson_list1
        assignment = queryset[int(index)-1][2]

    if is_teacher(request.user, classroom_id):
        if user_id and action and lesson and index:
            user = User.objects.get(id=user_id)
        if action == "set":
            try:
                assistant = WorkAssistant.objects.get(student_id=user_id, classroom_id=classroom_id, lesson_id=lesson, index=index)
            except ObjectDoesNotExist:
                assistant = WorkAssistant(student_id=user_id, classroom_id=classroom_id, lesson_id=lesson, index=index)
            assistant.save()

            # create Message
            group = Enroll.objects.get(classroom_id=classroom_id, student_id=assistant.student_id).group
            title = "<" + assistant.student.first_name.encode("utf-8") + u">擔任小老師<".encode("utf-8") + assignment + ">"
            url = "/teacher/score_peer/" + str(lesson) + "/" + index + "/"+ classroom_id + "/" + str(group)

            message = Message(title=title, url=url, time=timezone.now())
            message.save()
        else:
            try:
                assistant = WorkAssistant.objects.get(student_id=user_id, classroom_id=classroom_id, lesson_id=lesson, index=index)
                assistant.delete()
            except ObjectDoesNotExist:
                pass
            # create Message
            title = "<" + assistant.student.first_name.encode("utf-8") + u">取消小老師<".encode("utf-8") + assignment + ">"
            url = "/student/group/work/" + lesson + "/" + index + "/" + classroom_id
            message = Message(title=title, url=url, time=timezone.now())
            message.save()

        group = Enroll.objects.get(classroom_id=classroom_id, student_id=assistant.student_id).group
        if group > 0 :
            enrolls = Enroll.objects.filter(group = group)
            for enroll in enrolls:
                # message for group member
                messagepoll = MessagePoll(message_id = message.id,reader_id=enroll.student_id)
                messagepoll.save()
            return JsonResponse({'status':'ok'}, safe=False)
        else:
            return JsonResponse({'status':'n!'}, safe=False)
    else:
        return JsonResponse({'status':classroom_id}, safe=False)
# Create your views here.
def import_sheet(request):
    if False:
        return redirect("/")
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            ImportUser.objects.all().delete()
            request.FILES['file'].save_to_database(
                name_columns_by_row=0,
                model=ImportUser,
                mapdict=['username', 'first_name', 'password'])
            users = ImportUser.objects.all()
            return render(request, 'teacher/import_student.html',{'users':users})
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'teacher/import_form.html',
        {
            'form': form,
            'title': 'Excel file upload and download example',
            'header': ('Please choose any excel file ' +
                       'from your cloned repository:')
        })

# Create your views here.
def import_student(request):
    if False:
        return redirect("/")

    users = ImportUser.objects.all()
    username_list = [request.user.username+"_"+user.username for user in users]
    exist_users = [user.username for user in User.objects.filter(username__in=username_list)]
    create_list = []
    for user in users:
        username = request.user.username+"_"+user.username
        if username in exist_users:
            continue
        new_user = User(username=username, first_name=user.first_name, last_name=request.user.last_name, password=user.password, email=username+"@edu.tw")
        new_user.set_password(user.password)
        create_list.append(new_user)

    User.objects.bulk_create(create_list)
    new_users = User.objects.filter(username__in=[user.username for user in create_list])

    profile_list = []
    message_list = []
    poll_list = []
    title = "請洽詢任課教師課程名稱及選課密碼"
    url = "/student/classroom/add"
    message = Message(title=title, url=url, time=timezone.now())
    message.save()
    for user in new_users:
        profile = Profile(user=user)
        profile_list.append(profile)
        poll = MessagePoll(message_id=message.id, reader_id=user.id)
        poll_list.append(poll)

    Profile.objects.bulk_create(profile_list)
    MessagePoll.objects.bulk_create(poll_list)

    return redirect('/teacher/student/list')

# 教師可以查看所有帳號
class StudentListView(ListView):
    context_object_name = 'users'
    paginate_by = 50
    template_name = 'teacher/student_list.html'

    def get_queryset(self):
        username = username__icontains=self.request.user.username+"_"
        if self.request.GET.get('account') != None:
            keyword = self.request.GET.get('account')
            queryset = User.objects.filter(Q(username__icontains=username+keyword) | (Q(first_name__icontains=keyword) & Q(username__icontains=username))).order_by('-id')
        else :
            queryset = User.objects.filter(username__icontains=username).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        account = self.request.GET.get('account')
        context.update({'account': account})
        return context

# 修改密碼
def password(request, user_id):
    user = User.objects.get(id=user_id)
    if not user.username.startswith(request.user.username):
        return redirect("/")
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.set_password(request.POST['password'])
            user.save()
            return redirect('/teacher/student/list/')
    else:
        form = PasswordForm()
        user = User.objects.get(id=user_id)

    return render_to_response('form.html',{'form': form, 'user':user}, context_instance=RequestContext(request))

# 修改真實姓名
def realname(request, user_id):
    user = User.objects.get(id=user_id)
    if not user.username.startswith(request.user.username):
        return redirect("/")
    if request.method == 'POST':
        form = RealnameForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.first_name =form.cleaned_data['first_name']
            user.save()
            return redirect('/teacher/student/list/')
    else:
        teacher = False
        enrolls = Enroll.objects.filter(student_id=user_id)
        for enroll in enrolls:
            classroom = Classroom.objects.get(id=enroll.classroom_id)
            if request.user.id == classroom.teacher_id:
                teacher = True
                break
        if teacher or request.user.is_superuser:
            user = User.objects.get(id=user_id)
            form = RealnameForm(instance=user)
        else:
            return redirect("/")

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))
  
# 列出所有課程
class WorkListView2(ListView):
    model = TWork
    context_object_name = 'works'
    template_name = 'teacher/twork_list.html'  	
    paginate_by = 20
	
    def get_queryset(self):
        queryset = TWork.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        return queryset
			
    def get_context_data(self, **kwargs):
        context = super(WorkListView2, self).get_context_data(**kwargs)
        context['classroom'] = Classroom.objects.get(id=self.kwargs['classroom_id'])
        context['lesson'] = self.kwargs['lesson']
        return context	
        
#新增一個課程
class WorkCreateView2(CreateView):
    model = TWork
    form_class = WorkForm
    template_name = 'form.html'  	    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.teacher_id = self.request.user.id
        self.object.classroom_id = self.kwargs['classroom_id']
        self.object.save()              
        return redirect("/teacher/work2/"+self.kwargs['lesson']+"/"+self.kwargs['classroom_id'])        
        
# 修改選課密碼
def work_edit(request, classroom_id):
    # 限本班任課教師
    if not is_teacher(request.user, classroom_id):
        return redirect("homepage")
    classroom = Classroom.objects.get(id=classroom_id)
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom.name =form.cleaned_data['name']
            classroom.password = form.cleaned_data['password']
            classroom.save()
            # 記錄系統事件
            if is_event_open(request) :                
                log = Log(user_id=request.user.id, event=u'修改選課密碼<'+classroom.name+'>')
                log.save()                    
            return redirect('/teacher/classroom')
    else:
        form = ClassroomForm(instance=classroom)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))        
  
# 列出某作業所有同學名單
def work_class2(request, lesson, classroom_id, work_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    classroom = Classroom.objects.get(id=classroom_id)
    classmate_work = []
    scorer_name = ""
    for enroll in enrolls:
        try:    
            work = Work.objects.get(typing=1, user_id=enroll.student_id, index=work_id, lesson_id=lesson)
            if work.scorer > 0 :
                scorer = User.objects.get(id=work.scorer)
                scorer_name = scorer.first_name
            else :
                scorer_name = "1"
        except ObjectDoesNotExist:
            work = Work(typing=1, index=work_id, user_id=0, lesson_id=lesson)
        except MultipleObjectsReturned:
            work = Work.objects.filter(typing=1, user_id=enroll.student_id, index=work_id, lesson_id=lesson).last()			
        try:
            group_name = EnrollGroup.objects.get(id=enroll.group).name
        except ObjectDoesNotExist:
            group_name = "沒有組別"
        assistant = WorkAssistant.objects.filter(typing=1, classroom_id=classroom_id, student_id=enroll.student_id, lesson_id=lesson, index=work_id)
        if assistant.exists():
            classmate_work.append([enroll,work,1, scorer_name, group_name])
        else :
            classmate_work.append([enroll,work,0, scorer_name, group_name])   
    def getKey(custom):
        return custom[0].seat
	
    classmate_work = sorted(classmate_work, key=getKey)    
       
    return render_to_response('teacher/work_class.html',{'typing':1, 'classmate_work': classmate_work, 'classroom':classroom, 'index': work_id}, context_instance=RequestContext(request))
	
