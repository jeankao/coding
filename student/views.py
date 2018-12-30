# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
#from django.contrib.auth import authenticate, login
from django.template import RequestContext
from student.lesson import *
from django.views.generic import ListView, CreateView
from student.models import *
from teacher.models import *
from show.models import Round
from account.models import Message, MessagePoll, Profile, VisitorLog, PointHistory, LessonCounter, DayCounter, LogCounter
from account.avatar import *
from student.forms import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from wsgiref.util import FileWrapper
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from binascii import a2b_base64
import os
from datetime import datetime, timedelta
from time import localtime
import pytz
from django.core.paginator import Paginator
import copy
import jieba
from django.db.models import Q
import json

# 判斷是否為授課教師
def is_teacher(user, classroom_id):
    return user.groups.filter(name='teacher').exists() and Classroom.objects.filter(teacher_id=user.id, id=classroom_id).exists()

# 判斷是否為同班同學
def is_classmate(user, classroom_id):
    enroll_pool = [enroll for enroll in Enroll.objects.filter(classroom_id=classroom_id).order_by('seat')]
    student_ids = map(lambda a: a.student_id, enroll_pool)
    return user.id in student_ids

# 課程瀏覽記錄
def statics_lesson(request, lesson):
    try :
        counter = LessonCounter.objects.get(name=lesson)
        counter.hit = counter.hit + 1
    except ObjectDoesNotExist:
        counter = LessonCounter(name=lesson, hit=1)
    except MultipleObjectsReturned:
        counters = LessonCounter.objects.filter(name=lesson)
        counter = counter[0]
        counter.hit = counter.hit + 1
    counter.save()
    day = str(datetime.now())[0:4]+str(datetime.now())[5:7]+str(datetime.now())[8:10]
    try :
        daycounter = DayCounter.objects.get(day=day)
        daycounter.hit = daycounter.hit + 1
    except ObjectDoesNotExist:
        daycounter = DayCounter(day=day, hit=1)
    except MultipleObjectsReturned:
        daycounters = DayCounter.objects.filter(day=day)
        daycounter = daycounters[0]
        daycounter.hit = daycounter.hit + 1
    daycounter.save()
    log = LogCounter(counter_id=counter.id, counter_ip=request.META['REMOTE_ADDR'])
    log.save()
    return counter.hit


# 各種課程
def lessons(request, subject_id):
    hit = statics_lesson(request, subject_id)
    if request.user.is_authenticated():
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        if subject_id == "A":
            lock = profile.lock1
        elif subject_id == "B":
            lock = profile.lock2
        elif subject_id == "C":
            lock = profile.lock3
        elif subject_id == "D":
            lock = profile.lock4
        elif subject_id == "E":
            lock = profile.lock5
        else:
            lock = profile.lock1
    else :
        user_id = 0
        lock = 1
    return render(request, 'student/lessons.html', {'subject_id': subject_id, 'counter': hit, 'lock':lock})

# 課程內容
def lesson(request, lesson):
    work_dict = {}
    hit = statics_lesson(request, lesson)

    if request.user.id > 0 :
        profile = Profile.objects.get(user=request.user)
    else:
        profile = Profile()
    if lesson[0] == "A":
        lesson_id = 1
        profile_lock = profile.lock1
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(typing=0, lesson_id=lesson_id, user_id=request.user.id)))
        # 限登入者
        if not request.user.id > 0:
            return redirect("/account/login/0")
        else :
            lock = {'A002':2, 'A003':3, 'A004':5, 'A005':7, 'A006':9, 'A007':11, 'A008':13, 'A009':14, 'A010':15, 'A011':16}
        if lesson in lock:
            if profile_lock < lock[lesson]:
                if not request.user.groups.filter(name='teacher').exists():
                    return redirect("/")
        return render(request, 'student/lessonA.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':"0" })
    elif lesson[0] == "B":
        lesson_id = 2
        profile_lock = profile.lock2
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(typing=0, lesson_id=lesson_id, user_id=request.user.id)))
        # 限登入者
        if not request.user.is_authenticated():
            return redirect("/account/login/0")
        else :
            lock = {'B02':3, 'B03':4, 'B04':5, 'B05':6, 'B06':7, 'B07':8, 'B08':9, 'B09':10, 'B10':11, 'B11':12, 'B12':13, 'B13':14, 'B14':15, 'B15':16, 'B16':17, 'B17':17, 'B18':17}
        if lesson in lock:
            if profile_lock < lock[lesson]:
                if not request.user.groups.filter(name='teacher').exists():
                    return redirect("/")

        return render(request, 'student/lessonB.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':"0"})
    elif lesson[0] == "C":
        lesson_id = 3
        profile_lock = profile.lock3
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(lesson_id=lesson_id, user_id=request.user.id)))
        return render(request, 'student/lessonC.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':"0"})
    elif lesson[0] == "D":
        lesson_id = 4
        profile_lock = profile.lock4
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(lesson_id=lesson_id, user_id=request.user.id)))
        return render(request, 'student/lessonD.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':"0"})
    elif lesson[0] == "E":
        lesson_id = 5
        profile_lock = profile.lock5
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(typing=0, lesson_id=lesson_id, user_id=request.user.id)))
        # 限登入者
        if not request.user.is_authenticated():
            return redirect("/account/login/0")
        else :
            lock = {'E02':3, 'E03':4, 'E04':5, 'E05':6, 'E06':7, 'E07':8, 'E08':9, 'E09':10, 'E10':11, 'E11':12, 'E12':13, 'E13':14, 'E14':15, 'E15':16, 'E16':17, 'E17':17, 'E18':17}
        if lesson in lock:
            if profile_lock < lock[lesson]:
                if not request.user.groups.filter(name='teacher').exists():
                    return redirect("/")

        return render(request, 'student/lessonE.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':"0"})
    elif lesson[0] == "G":
        lesson_id = 7
        #profile_lock = profile.lock5
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(typing=0, lesson_id=lesson_id, user_id=request.user.id)))
        # 限登入者
        #if not request.user.is_authenticated():
        #    return redirect("/account/login/0")
        #else :
        #    pass
            #lock = {'E02':3, 'E03':4, 'E04':5, 'E05':6, 'E06':7, 'E07':8, 'E08':9, 'E09':10, 'E10':11, 'E11':12, 'E12':13, 'E13':14, 'E14':15, 'E15':16, 'E16':17, 'E17':17, 'E18':17}
        #if lesson in lock:
        #    if profile_lock < lock[lesson]:
        #        if not request.user.groups.filter(name='teacher').exists():
        #            return redirect("/")

        return render(request, 'student/lessonG.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':"0"})
    else:
        lesson_id = 1
        profile_lock = profile.lock1
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(lesson_id=lesson_id, user_id=request.user.id)))
        return render(request, 'student/lessonA.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':"0"})

# 查看班級學生
def classmate(request, classroom_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    enroll_group = []
    classroom=Classroom.objects.get(id=classroom_id)
    for enroll in enrolls:
        login_times = len(VisitorLog.objects.filter(user_id=enroll.student_id))
        if enroll.group > 0 :
            enroll_group.append([enroll, EnrollGroup.objects.get(id=enroll.group).name, login_times])
        else :
            enroll_group.append([enroll, "沒有組別", login_times])

    return render(request, 'student/classmate.html', {'classroom':classroom, 'enrolls':enroll_group})

# 顯示所有組別
def group(request, classroom_id):
    student_groups = []
    classroom = Classroom.objects.get(id=classroom_id)
    group_open = Classroom.objects.get(id=classroom_id).group_open
    groups = EnrollGroup.objects.filter(classroom_id=classroom_id)
    try:
            student_group = Enroll.objects.get(student_id=request.user.id, classroom_id=classroom_id).group
    except ObjectDoesNotExist :
            student_group = []
    for group in groups:
        enrolls = Enroll.objects.filter(classroom_id=classroom_id, group=group.id)
        student_groups.append([group, enrolls, classroom.group_size-len(enrolls)])

    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    nogroup = []
    for enroll in enrolls:
        if enroll.group == 0 :
            nogroup.append(enroll)
    nogroup = sorted(nogroup, key=lambda s: s.seat)
    return render(request, 'student/group.html', {'nogroup': nogroup, 'group_open': group_open, 'student_groups':student_groups, 'classroom':classroom, 'student_group':student_group, 'teacher': is_teacher(request.user, classroom_id)})

# 新增組別
def group_add(request, classroom_id):
    if request.method == 'POST':
        classroom_name = Classroom.objects.get(id=classroom_id).name
        form = GroupForm(request.POST)
        if form.is_valid():
            group = EnrollGroup(name=form.cleaned_data['name'],classroom_id=int(classroom_id))
            group.save()

            return redirect('/student/group/'+classroom_id)
    else:
        form = GroupForm()
    return render(request, 'form.html', {'form':form})

# 設定組別人數
def group_size(request, classroom_id):
    if request.method == 'POST':
        form = GroupSizeForm(request.POST)
        if form.is_valid():
            classroom = Classroom.objects.get(id=classroom_id)
            classroom.group_size = form.cleaned_data['group_size']
            classroom.save()

            return redirect('/student/group/'+classroom_id)
    else:
        classroom = Classroom.objects.get(id=classroom_id)
        form = GroupSizeForm(instance=classroom)
    return render(request, 'form.html', {'form':form})

# 加入組別
def group_enroll(request, classroom_id,  group_id):
    classroom = Classroom.objects.get(id=classroom_id)
    members = Enroll.objects.filter(group=group_id)
    if len(members) < classroom.group_size:
        group_name = EnrollGroup.objects.get(id=group_id).name
        enroll = Enroll.objects.filter(student_id=request.user.id, classroom_id=classroom_id)
        enroll.update(group=group_id)

    return redirect('/student/group/'+classroom_id)

# 刪除組別
def group_delete(request, group_id, classroom_id):
    group = EnrollGroup.objects.get(id=group_id)
    group.delete()
    classroom_name = Classroom.objects.get(id=classroom_id).name

    return redirect('/student/group/'+classroom_id)

# 是否開放選組
def group_open(request, classroom_id, action):
    classroom = Classroom.objects.get(id=classroom_id)
    if action == "1":
        classroom.group_open=True
        classroom.save()
    else :
        classroom.group_open=False
        classroom.save()

    return redirect('/student/group/'+classroom_id)

# 列出選修的班級
class ClassroomList(ListView):
    context_object_name = 'classrooms'
    paginate_by = 30
    template_name = 'student/classroom.html'

    def get_queryset(self):
        classrooms = []
        enrolls = Enroll.objects.filter(student_id=self.request.user.id).order_by("-id")
        round_pool = Round.objects.all().order_by("-id")
        for enroll in enrolls :
            shows = filter(lambda w: w.classroom_id == enroll.classroom_id, round_pool)
            classrooms.append([enroll, shows])
        return classrooms

# 查看班級
class ClassroomAdd(ListView):
    context_object_name = 'classroom_teachers'
    paginate_by = 30
    template_name = 'student/classroom_add.html'

    def get_queryset(self):
        if self.request.GET.get('account') != None:
            keyword = self.request.GET.get('account')
            queryset = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword)).order_by('-id')
        else :
            queryset = User.objects.filter(groups__name='teacher')
        teacher_ids = map(lambda a: a.id, queryset)
        classrooms = Classroom.objects.filter(teacher_id__in=teacher_ids).order_by('-id')
        classroom_teachers = []
        for classroom in classrooms:
            enroll = Enroll.objects.filter(student_id=self.request.user.id, classroom_id=classroom.id)
            if enroll.exists():
                classroom_teachers.append([classroom,classroom.teacher.first_name,1])
            else:
                classroom_teachers.append([classroom,classroom.teacher.first_name,0])
        return classroom_teachers

# 加入班級
def classroom_enroll(request, classroom_id):
    scores = []
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            try:
                classroom = Classroom.objects.get(id=classroom_id)
                if classroom.password == form.cleaned_data['password']:
                    try:
                        enroll = Enroll.objects.get(classroom_id=classroom_id, student_id=request.user.id)
                    except ObjectDoesNotExist:
                        enroll = Enroll(classroom_id=classroom_id, student_id=request.user.id, seat=form.cleaned_data['seat'])
                    enroll.save()
                else:
                    return render(request, 'message.html', {'message':"選課密碼錯誤"})
            except Classroom.DoesNotExist:
                pass
            return redirect("/student/group/" + str(classroom.id))
    else:
        form = EnrollForm()
    return render(request, 'form.html', {'form':form})

# 修改座號
def seat_edit(request, enroll_id, classroom_id):
    enroll = Enroll.objects.get(id=enroll_id)
    if request.method == 'POST':
        form = SeatForm(request.POST)
        if form.is_valid():
            enroll.seat =form.cleaned_data['seat']
            enroll.save()
            classroom_name = Classroom.objects.get(id=classroom_id).name
            return redirect('/student/classroom')
    else:
        form = SeatForm(instance=enroll)

    return render(request, 'form.html',{'form': form})

# 登入記錄
class LoginLogListView(ListView):
    context_object_name = 'visitorlogs'
    paginate_by = 20
    template_name = 'student/login_log.html'
    def get_queryset(self):
        visitorlogs = VisitorLog.objects.filter(user_id=self.kwargs['user_id']).order_by("-id")
        return visitorlogs

    def get_context_data(self, **kwargs):
        context = super(LoginLogListView, self).get_context_data(**kwargs)
        if self.request.GET.get('page') :
            context['page'] = int(self.request.GET.get('page')) * 20 - 20
        else :
            context['page'] = 0
        return context

# 列出所有公告
class AnnounceListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'student/announce_list.html'
    paginate_by = 20

    def get_queryset(self):
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])

        messages = Message.objects.filter(classroom_id=self.kwargs['classroom_id'], author_id=classroom.teacher_id).order_by("-id")
        queryset = []
        for message in messages:
            messagepoll = MessagePoll.objects.get(message_id=message.id, reader_id=self.request.user.id)
            queryset.append([messagepoll, message])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AnnounceListView, self).get_context_data(**kwargs)
        context['classroom'] = Classroom.objects.get(id=self.kwargs['classroom_id'])
        return context

    # 限本班同學
    def render(request, self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(AnnounceListView, self).render(request, context)

# 列出個人所有作業
def work_list(request, typing, lesson, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lessons = []

    if typing == "0":
        if lesson in ["2", "3", "4", "5", "6", "7", "8", "9"]:
            assignments = [lesson_list2, lesson_list3, lesson_list4, lesson_list2, lesson_list2, lesson_list2, lesson_list5, lesson_list2][int(lesson)-2]
        else:
            assignments = lesson_list1
    elif typing == "1":
        assignments = TWork.objects.filter(classroom_id=classroom_id).order_by("-id")
    elif typing == "2":
        assignments = CWork.objects.filter(classroom_id=classroom_id).order_by("-id")
    else :
        assignments = TWork.objects.filter(classroom_id=classroom_id).order_by("-id")
    work_dict = dict(((work.index, work) for work in Work.objects.filter(typing=typing, user_id=request.user.id, lesson_id=lesson)))

    for idx, assignment in enumerate(assignments):
        if typing == "0":
            index = idx+1
        elif typing == "1":
            index = assignment.id
        elif typing == "2":
            index = assignment.id
        else :
            index = assignment.id
        if not index in work_dict:
            lessons.append([assignment, None])
        else:
           lessons.append([assignment, work_dict[index]])
    return render(request, 'student/work_list.html', {'typing':typing, 'lesson':lesson, 'lessons':lessons, 'classroom':classroom})

def submit(request, typing, lesson, index):
    work_dict = {}
    form = None
    work_dict = dict(((int(work.index), [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(typing=typing, lesson_id=lesson, user_id=request.user.id)))
    if typing == "0":
        if lesson in ["2", "3", "4", "5", "6", "7", "8", "9"]:
            lesson_name = [lesson_list2, lesson_list3, lesson_list4, lesson_list2, lesson_list2, lesson_list2, lesson_list5, lesson_list2][int(lesson)-2][int(index)-1][1]
        else:
            lesson_name = lesson_list1[int(index)-1][2]
    elif typing == "1":
        lesson_name = TWork.objects.get(id=index).title

    if lesson == "1" or lesson == "6":
        works = Work.objects.filter(typing=typing, index=index, user_id=request.user.id, lesson_id=lesson)
        try:
            filepath = request.FILES['file']
        except :
            filepath = False
        if request.method == 'POST':
            if filepath :
                myfile = request.FILES['file']
                if lesson == "6":
                    fs = FileSystemStorage(settings.BASE_DIR+"/static/work/microbit/"+str(request.user.id)+"/")
                else :
                    fs = FileSystemStorage(settings.BASE_DIR+"/static/work/scratch/"+str(request.user.id)+"/")
                filename = uuid4().hex
                fs.save(filename, myfile)
            form = SubmitAForm(request.POST, request.FILES)
            if not works.exists():
                if form.is_valid():
                    work = Work(typing=typing, lesson_id=lesson, index=index, user_id=request.user.id, memo=form.cleaned_data['memo'])
                    work.save()
                    workfile = WorkFile(work_id=work.id, filename=filename)
                    workfile.save()
                    # credit
                    update_avatar(request.user.id, 1, 2)
                    # History
                    history = PointHistory(user_id=request.user.id, kind=1, message=u'2分--繳交作業<'+lesson_name+'>', url=request.get_full_path().replace("submit", "submitall"))
                    history.save()
                    if typing == "0":
                        # lock
                        profile = Profile.objects.get(user=request.user)
                        profile.lock1 += 1
                        profile.save()
            else:
                if form.is_valid():
                    works.update(memo=form.cleaned_data['memo'][0:500],publication_date=timezone.localtime(timezone.now()))
                    workfile = WorkFile(work_id=works[0].id, filename=filename)
                    workfile.save()
                else :
                    works.update(memo=form.cleaned_data['memo'])
            return redirect("/student/work/show/"+typing+"/"+lesson+"/"+index+"/"+str(request.user.id))
    elif lesson == "4":
        if request.method == 'POST':
            form = SubmitCForm(request.POST)
            if form.is_valid():
                try:
                    work = Work.objects.get(typing=typing, lesson_id=lesson, index=index, user_id=request.user.id)
                except ObjectDoesNotExist:
                    # credit
                    answers = Answer.objects.filter(lesson_id=lesson, index=index, student_id=request.user.id)
                    if len(answers)>0 :
                        points = 1
                    else :
                        points = 3
                    update_avatar(request.user.id, 1, points)
                    # History
                    history = PointHistory(user_id=request.user.id, kind=1, message=str(points)+'分--繳交作業<'+lesson_name+'>', url="/student/work/show/"+lesson+"/"+index)
                    history.save()
                    profile = Profile.objects.get(user=request.user)
                    if typing == "0":
                        profile.lock4 +=1
                        profile.save()
                except MultipleObjectsReturned:
                    pass
                work = Work(typing=typing, lesson_id=lesson, index=index, user_id=request.user.id)
                work.youtube=form.cleaned_data['youtube']
                work.memo=form.cleaned_data['memo'][0:500]
                work.save()
                return redirect("/student/work/show/"+typing+"/"+lesson+"/"+index+"/"+str(request.user.id))
            return redirect('/student/lesson/'+request.POST.get("lesson", ""))
    elif lesson == "2" or lesson == "3" or lesson == "5" or lesson == "7" or lesson == "8":
        if request.method == 'POST':
            if lesson == "8":
                form = SubmitDForm(request.POST, request.FILES)
            else :
                form = SubmitBForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    work = Work.objects.get(typing=typing, lesson_id=lesson, index=index, user_id=request.user.id)
                except ObjectDoesNotExist:
                    # credit
                    answers = Answer.objects.filter(lesson_id=lesson, index=index, student_id=request.user.id)
                    if len(answers)>0 :
                        points = 1
                    else :
                        points = 3
                    update_avatar(request.user.id, 1, points)
                    # History
                    history = PointHistory(user_id=request.user.id, kind=1, message=str(points)+'分--繳交作業<'+lesson_name+'>', url="/student/work/show/"+lesson+"/"+index)
                    history.save()
                    profile = Profile.objects.get(user=request.user)
                    if typing == "0":
                        if lesson == "2":
                            profile.lock2 += 1
                        elif lesson == "3":
                            profile.lock3 +=1
                        elif lesson == "5":
                            profile.lock5 +=1
                        elif lesson == "8":
                            profile.lock6 +=1
                        else:
                            profile.lock3 += 1
                        profile.save()
                except MultipleObjectsReturned:
                    pass
                work = Work(typing=typing, lesson_id=lesson, index=index, user_id=request.user.id)
                work.save()

                dataURI = form.cleaned_data['screenshot']
                try:
                    head, data = dataURI.split(',', 1)
                    mime, b64 = head.split(';', 1)
                    mtype, fext = mime.split('/', 1)
                    binary_data = a2b_base64(data)

                    prefix = ['static/work/vphysics', 'static/work/euler', 'static/work/ck', 'static/work/vphysics2', '', 'static/work/pandas', 'static/work/django'][int(lesson) - 2]
                    directory = "{prefix}/{uid}/{index}".format(prefix=prefix, uid=request.user.id, index=index)
                    image_file = "{path}/{id}.jpg".format(path=directory, id=work.id)

                    if not os.path.exists(settings.BASE_DIR + "/" + directory):
                        os.makedirs(settings.BASE_DIR + "/" + directory)
                    with open(settings.BASE_DIR + "/" + image_file, 'wb') as fd:
                        fd.write(binary_data)
                        fd.close()
                    work.picture=image_file
                except ValueError:
                    path = dataURI.split('/', 3)
                    work.picture=path[3]
                    pass
                if lesson == "8":
                    work.memo=form.cleaned_data['memo'][0:500]
                else :
                    work.code=form.cleaned_data['code']
                    work.memo=form.cleaned_data['memo'][0:500]
                    work.helps=form.cleaned_data['helps']
                work.save()
                return redirect("/student/work/show/"+typing+"/"+lesson+"/"+index+"/"+str(request.user.id))
            return redirect('/student/lesson/'+request.POST.get("lesson", ""))
    elif lesson == "9":
        if request.method == 'POST':
            if typing == "1":
                types = request.POST.get('types')
                index = request.POST.get('index')
                q_index = request.POST.get('q_index')
                question_id = request.POST.get('question_id')
                if types == "11" or types == "12":
                    form = SubmitF1Form(request.POST, request.FILES)
                    if form.is_valid():
                        obj = form.save(commit=False)
                        try:
                            work = Science1Work.objects.get(student_id=request.user.id, index=index, question_id=question_id)
                        except ObjectDoesNotExist:
                            work = Science1Work(student_id=request.user.id, index=index, question_id=question_id)
                        except MultipleObjectsReturned:
                            works = Science1Work.objects.filter(student_id=request.user.id, index=index, question_id=question_id).order_by("-id")
                            work = work[0]
                        work.publication_date = timezone.now()
                        work.save()
                        obj.work_id=work.id
                        if types == "12":
                            myfile = request.FILES['pic']
                            fs = FileSystemStorage(settings.BASE_DIR+"/static/upload/"+str(request.user.id)+"/")
                            filename = uuid4().hex
                            obj.picname = str(request.user.id)+"/"+filename
                            fs.save(filename, myfile)
                        obj.pic = ""
                        obj.save()
                        return redirect("/student/work/submit/"+typing+"/"+lesson+"/"+index+"/#question"+q_index)
                elif types in ["21", "22"]: # 資料建模, 流程建模
                    form = SubmitF2Form(request.POST)
                    model_type = int(types == "22")
                    if form.is_valid():
                        jsonid = request.POST['jsonid']
                        if jsonid:
                            try:
                                json = Science2Json.objects.get(id=jsonid)
                            except ObjectDoesNotExist:
                                json = Science2Json(index=index, student_id=request.user.id, model_type=model_type)
                        else:
                            json = Science2Json(index=index, student_id=request.user.id, model_type=model_type)

                        json.json = request.POST['jsonstr']
                        json.save()
                        return redirect("/student/work/submit/"+typing+"/"+lesson+"/"+index+"/#tab"+types)
                    return redirect('/')
                elif types == "3":
                    form = SubmitF3Form(request.POST, request.FILES)
                    if form.is_valid():
                        work = Science3Work(index=index, student_id=request.user.id)
                        work.save()                        

                        dataURI = form.cleaned_data['screenshot']
                        try:
                            head, data = dataURI.split(',', 1)
                            mime, b64 = head.split(';', 1)
                            mtype, fext = mime.split('/', 1)
                            binary_data = a2b_base64(data)

                            prefix = 'static/work/science'
                            directory = "{prefix}/{uid}/{index}".format(prefix=prefix, uid=request.user.id, index=index)
                            image_file = "{path}/{id}.jpg".format(path=directory, id=work.id)

                            if not os.path.exists(settings.BASE_DIR + "/" + directory):
                                os.makedirs(settings.BASE_DIR + "/" + directory)
                            with open(settings.BASE_DIR + "/" + image_file, 'wb') as fd:
                                fd.write(binary_data)
                                fd.close()
                            work.picture=image_file
                        except ValueError:
                             path = dataURI.split('/', 3)
                             work.picture=path[3]

                        work.code=form.cleaned_data['code']
                        work.helps=form.cleaned_data['helps']
                        work.save()
                        return redirect("/student/work/submit/"+typing+"/"+lesson+"/"+index+"/#tab3")
                elif types == "41":
                    form = SubmitF4Form(request.POST)
                    if form.is_valid():
                        try:
                            work = Science4Work.objects.get(student_id=request.user.id, index=index)
                        except ObjectDoesNotExist:
                            work = Science4Work(student_id=request.user.id, index=index)
                        except MultipleObjectsReturned:
                            works = Science4Work.objects.filter(student_id=request.user.id, index=index).order_by("-id")
                            work = work[0]
                        work.memo = form.cleaned_data['memo']
                        work.save()
                        return redirect("/student/work/submit/"+typing+"/"+lesson+"/"+index+"/#tab4")
                elif types == "42":
                    form = SubmitF4BugForm(request.POST)
                    if form.is_valid():
                        obj = form.save(commit=False)

                        return redirect("/")
        else:
            contents1 = [[]]
            works_pool = Science1Work.objects.filter(student_id=request.user.id, index=index).order_by("-id")
            questions = Science1Question.objects.filter(work_id=index)
            for question in questions:
                works = filter(lambda w: w.question_id==question.id, works_pool)
                if len(works) > 0:
                    contents = Science1Content.objects.filter(work_id=works[0].id).order_by("id")
                    if len(contents)>0:
                        contents1.append([contents])
                    else:
				        contents1.append([[]])
                else:
				    contents1.append([[]])
            works3 = Science3Work.objects.filter(student_id=request.user.id, index=index).order_by("id")  
            work3_ids = [work.id for work in works3]            
            if works3.exists():
                work3 = works3[0]
            else :
                work3 = Science3Work(student_id=request.user.id, index=index)
            try:
                work4 = Science4Work.objects.get(student_id=request.user.id, index=index)
            except ObjectDoesNotExist:
                work4 = Science4Work(student_id=request.user.id, index=index)
            except MultipleObjectsReturned:
                works4 = Science4Work.objects.filter(student_id=request.user.id, index=index).order_by("-id")
                work4 = works[0]
            contents4 = Science4Debug.objects.filter(work3_id__in=work3_ids).order_by("-id")                
            try:
                expr = Science2Json.objects.get(student_id=request.user.id, index=index, model_type=0)
            except ObjectDoesNotExist:
                expr = Science2Json(student_id=request.user.id, index=index, model_type=0, json='{vars:[], arrs:[], exprs:[]}')
            try:
                flow = Science2Json.objects.get(student_id=request.user.id, index=index, model_type=1)
            except ObjectDoesNotExist:
                flow = Science2Json(student_id=request.user.id, index=index, model_type=1, json='[]')
            questions = Science1Question.objects.filter(work_id=index)
            return render(request, 'student/submit.html', {'form':form, 'questions':questions, 'typing':typing, 'lesson': lesson, 'index':index, 'contents1':contents1, 'contents4':contents4, 'work3':work3, 'works3':works3, 'work3_ids':work3_ids, 'work4': work4, 'expr': expr, 'flow': flow})

    return render(request, 'student/submit.html', {'form':form, 'typing':typing, 'lesson': lesson, 'lesson_id':lesson, 'index':index, 'work_dict':work_dict})

def show(request, typing, lesson, index, user_id):
    work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(typing=typing, lesson_id=lesson, user_id=request.user.id)))
    if int(user_id) == request.user.id or request.user.is_superuser:
        try:
            work = Work.objects.get(typing=typing, lesson_id=lesson, index=index, user_id=user_id)
        except ObjectDoesNotExist:
            work = None
        except MultipleObjectsReturned:
            work = Work.objects.filter(typing=typing, lesson_id=lesson, index=index, user_id=user_id).last()
        return render(request, 'student/show.html', {'work':work, 'lesson':lesson, 'work_dict':work_dict, 'index':index})
    else :
        return redirect("/")

def rank(request, typing, lesson, index):
    works = Work.objects.filter(typing=typing, lesson_id=lesson, index=index).order_by("id")
    return render(request, 'student/rank.html', {'works':works, 'lesson':lesson})

# 列出所有日期作品
class WorkListView(ListView):
    model = Work
    context_object_name = 'total_works'
    template_name = 'student/works_list.html'

    def get_queryset(self):
        if self.kwargs['lesson'] == "2":
            work_pool = Work.objects.filter(lesson_id__in=[2,4])
        else:
            work_pool = Work.objects.filter(lesson_id=self.kwargs['lesson'])
        queryset = []
        timezone = pytz.timezone("Asia/Taipei")
        start = timezone.localize(datetime(2018,4,1))
        end = timezone.localize(datetime.now())
        daterange = [start + timedelta(days=x) for x in range(0, (end-start).days+1)]
        for day in reversed(daterange):
            work = filter(lambda w: w.publication_date >= day and  w.publication_date < day+timedelta(days=1), work_pool)
            if len(work)>0 :
                queryset.append([day, len(work)])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WorkListView, self).get_context_data(**kwargs)
        start = datetime(2018,4,1)
        end = datetime.today()
        context['height'] = 200+ (end.year-start.year)*200
        context['lesson'] = self.kwargs['lesson']
        return context

# 列出某日所有作品
class WorkDayListView(ListView):
    model = Work
    context_object_name = 'works'
    template_name = 'student/works_day.html'
    paginate_by = 20

    def get_queryset(self):
        if self.kwargs['lesson'] == "2":
            work_pool = Work.objects.filter(lesson_id__in=[2,4]).order_by("-id")
        else:
            work_pool = Work.objects.filter(lesson_id=self.kwargs['lesson']).order_by("-id")
        timezone = pytz.timezone("Asia/Taipei")
        day = timezone.localize(datetime(int(self.kwargs['year']),int(self.kwargs['month']),int(self.kwargs['date'])))
        works = filter(lambda w: w.publication_date >= day and  w.publication_date < day+timedelta(days=1), work_pool)
        return works

    def get_context_data(self, **kwargs):
        context = super(WorkDayListView, self).get_context_data(**kwargs)
        context['lesson'] = self.kwargs['lesson']
        context['date'] = datetime(int(self.kwargs['year']),int(self.kwargs['month']),int(self.kwargs['date']))
        return context


# 查詢某作業所有同學心得
def memo(request, typing, lesson, classroom_id, index):
    enroll_pool = [enroll for enroll in Enroll.objects.filter(classroom_id=classroom_id).order_by('seat')]
    student_ids = map(lambda a: a.student_id, enroll_pool)
    work_pool = Work.objects.filter(typing=typing, lesson_id=lesson, user_id__in=student_ids, index=index).order_by("-id")
    datas = []
    for enroll in enroll_pool:
        works = filter(lambda w: w.user_id == enroll.student_id, work_pool)
        if works :
            datas.append([enroll, works[0].memo])
        else:
            datas.append([enroll, ""])

    return render(request, 'student/memo.html', {'lesson':lesson, 'classroom_id':classroom_id, 'datas': datas})

# 查詢某檢核作業所有同學
def work_class(request, typing, lesson, classroom_id, index):
    enroll_pool = [enroll for enroll in Enroll.objects.filter(classroom_id=classroom_id).order_by('seat')]
    student_ids = map(lambda a: a.student_id, enroll_pool)
    work_pool = Work.objects.filter(typing=typing, lesson_id=lesson, user_id__in=student_ids, index=index).order_by("-id")
    datas = []
    enrollgroup_dict = dict(((group.id, enrollgroup) for enrollgroup in EnrollGroup.objects.filter(classroom_id=classroom_id)))
    if enroll.group == 0 :
         group_name = "沒有組別"
    else :
        group_name = enrollgroup_dict[enroll.group].name

    for enroll in enroll_pool:
        works = filter(lambda w: w.user_id == enroll.student_id, work_pool)
        if works :
            datas.append([enroll, works[0].score, group_name])
        else:
            datas.append([enroll, "", group_name])

    return render(request, 'student/work_class.html', {'lesson':lesson, 'classroom_id':classroom_id, 'datas': datas})


def work_download(request, typing, lesson, index, user_id, workfile_id):
    workfile = WorkFile.objects.get(id=workfile_id)
    username = User.objects.get(id=user_id).first_name
    if typing == "0":
        if lesson in ["2", "3", "4", "5", "6"]:
            lesson_name = [lesson_list2, lesson_list3, lesson_list4, lesson_list2, lesson_list2][int(lesson)-2][int(index)-1][1]
        else:
            lesson_name = lesson_list1[int(index)-1][2]
    elif typing == "1":
        lesson_name = TWork.objects.get(id=index).title

    if lesson == "1":
        filename = username + "_" + lesson_name.decode("utf-8")  + ".sb2"
        download =  settings.BASE_DIR + "/static/work/scratch/" + str(user_id) + "/" + workfile.filename
    elif lesson == "6":
        filename = username + "_" + lesson_name.decode("utf-8")  + ".hex"
        download =  settings.BASE_DIR + "/static/work/microbit/" + str(user_id) + "/" + workfile.filename
    wrapper = FileWrapper(file( download, "rb" ))
    response = HttpResponse(wrapper, content_type = 'application/force-download')
    #response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename.encode('utf8'))
    response['Content-Length'] = os.path.getsize(download)
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
    #return render(request, 'student/download.html', {'download':download})

# 查詢作業進度
def progress(request, typing, lesson, unit, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    bars = []

    enroll_pool = [enroll for enroll in Enroll.objects.filter(classroom_id=classroom_id).order_by('seat')]
    student_ids = map(lambda a: a.student_id, enroll_pool)
    work_pool = Work.objects.filter(typing=typing, user_id__in=student_ids, lesson_id=lesson).order_by("-id")

    for enroll in enroll_pool:
      student_works = filter(lambda u: u.user_id == enroll.student_id, work_pool)
      bar = []
      index = 1
      lesson_list = []
      if typing == "0":
          if lesson == "1":
              if unit == "1":
                  lesson_list = lesson_list1[0:17]
              elif unit == "2":
                  lesson_list = lesson_list1[17:25]
                  index = 18
              elif unit == "3":
                  lesson_list = lesson_list1[25:33]
                  index = 26
              elif unit == "4":
                  lesson_list = lesson_list1[33:41]
                  index = 34
              else:
                  lesson_list = lesson_list1[0:17]
          elif lesson == "2":
              lesson_list = lesson_list2
          elif lesson == "3":
              lesson_list = lesson_list3
          elif lesson == "4":
              lesson_list = lesson_list4
          elif lesson == "5":
              lesson_list = lesson_list2
          else:
              lesson_list = lesson_list3
          for assignment in lesson_list:
            works = filter(lambda u: u.index == index, student_works)
            index = index + 1
            if len(works) > 0:
              bar.append([assignment, works[0]])
            else:
              bar.append([assignment, False])
          bars.append([enroll, bar])
      elif typing == "1":
          lesson_list = TWork.objects.filter(classroom_id=classroom_id)
          for assignment in lesson_list:
            works = filter(lambda u: u.index == assignment.id, student_works)
            index = index + 1
            if len(works) > 0:
              bar.append([assignment, works[0]])
            else:
              bar.append([assignment, False])
          bars.append([enroll, bar])
      elif typing == "2":
          lesson_list = CWork.objects.filter(classroom_id=classroom_id)
          for assignment in lesson_list:
            works = filter(lambda u: u.index == assignment.id, student_works)
            index = index + 1
            if len(works) > 0:
              bar.append([assignment, works[0]])
            else:
              bar.append([assignment, False])
          bars.append([enroll, bar])
    return render(request, 'student/progress.html', {'typing':typing, 'lesson':lesson, 'unit':unit, 'bars':bars,'classroom':classroom, 'lesson_list':lesson_list})

# 查詢某作業分組小老師
def work_group(request, typing, lesson, classroom_id):
    if lesson == "1":
        lesson_list = lesson_list1
    elif lesson == "2":
        lesson_list = lesson_list2
    elif lesson == "3":
        lesson_list = lesson_list3
    elif lesson == "4":
        lesson_list = lesson_list4
    elif lesson == "5":
        lesson_list = lesson_list2
    else :
        lesson_list = lesson_list1
    lessons = []
    index = 0
    for assignment in lesson_list:
        student_groups = []
        enrolls = Enroll.objects.filter(classroom_id=classroom_id, group=group)
        group_assistants = []
        assistants = []
        works = []
        scorer_name = ""
        for enroll in enrolls:
            try:
                work = Work.objects.get(user_id=enroll.student_id, index=lesson+1)
                if work.scorer > 0 :
                    scorer = User.objects.get(id=work.scorer)
                    scorer_name = scorer.first_name
                else :
                    scorer_name = "X"
            except ObjectDoesNotExist:
                work = Work(index=lesson, user_id=1)
            works.append([enroll, work.score, scorer_name, work.memo])
            try :
                assistant = Assistant.objects.get(student_id=enroll.student.id, classroom_id=classroom_id, lesson=lesson+1)
                group_assistants.append(enroll)
                assistants.append(enroll.student_id)
            except ObjectDoesNotExist:
                pass
        student_groups.append([group, works, group_assistants, assistants])
        lessons.append([lesson_list[index], student_groups])
        index = index + 1
    return render(request, 'student/work_group.html', {'lesson':lesson, 'lessons':lessons, 'classroom_id':classroom_id})

# 解答
def answer(request, lesson, index):
    answers = Answer.objects.filter(lesson_id=lesson, index=index, student_id=request.user.id)
    if len(answers) > 0:
        answer = True
    else:
        answer = False
    try:
        work = Work.objects.get(lesson_id=lesson, index=index, user_id=request.user.id)
    except ObjectDoesNotExist:
        work = Work(lesson_id=lesson, index=index, user_id=request.user.id)
    except MultipleObjectsReturned:
        work = Work.objects.filter(lesson_id=lesson, index=index, user_id=request.user.id).last()
    return render(request, 'student/answer.html', {'lesson':lesson, 'index':index, 'answer':answer, 'work':work})

# 解答
def answer_watch(request, lesson, index):
    answer = Answer(lesson_id=lesson, index=index, student_id=request.user.id)
    answer.save()
    return redirect("/student/work/answer/"+lesson+"/"+index)

# 測驗卷
def exam(request):
    # 限登入者
    if not request.user.is_authenticated():
        return redirect("/account/login/")
    else :
        return render(request, 'student/exam.html')

# 測驗卷得分
def exam_score(request):
    exams = Exam.objects.filter(student_id=request.user.id).order_by("-id")
    return render(request, 'student/exam_score.html', {'exams':exams} )

# 測驗卷檢查答案
def exam_check(request):
    exam_id = request.POST.get('examid')
    user_answer = request.POST.get('answer').split(",")
    if not exam_id in ["1", "2", "3"]:
        return JsonResponse({'status':'ko'}, safe=False)

    correct_answer_list = ["C,A,D,C,C,A,B,B,D,D", "B,C,C,A,D,B,A,D,B,C", "D,C,A,B,D,C,D,A,D,B"]
    answer = correct_answer_list[int(exam_id)-1]
    correct_answer = answer.split(",")
    ua_test = ""
    score = 0
    for i in range(10) :
        if user_answer[i] == correct_answer[i] :
            score = score + 10
    ua_test = "".join(user_answer)
    exam = Exam(exam_id=int(exam_id), student_id=request.user.id, answer=ua_test, score=score)
    exam.save()
    return JsonResponse({'status':'ok','answer':answer}, safe=False)

def memo_user(request, lesson, classroom_id, user_id):
    user = User.objects.get(id=user_id)
    if not is_classmate(user, classroom_id):
        return redirect("/")
    lesson_list = []
    del lesson_list[:]
    if lesson == "1":
        lesson_list = copy.deepcopy(lesson_list1)
    elif lesson == "2":
        lesson_list = copy.deepcopy(lesson_list2)
    elif lesson == "3":
        lesson_list = copy.deepcopy(lesson_list3)
    elif lesson == "4":
        lesson_list = copy.deepcopy(lesson_list4)
    elif lesson == "5":
        lesson_list = copy.deepcopy(lesson_list2)
    else :
        lesson_list = copy.deepcopy(lesson_list1)
    works = Work.objects.filter(lesson_id=lesson, user_id=user_id, typing=0).order_by("-id")
    for work in works:
        lesson_list[work.index-1].append(work.memo)

    tworks = TWork.objects.filter(classroom_id=classroom_id)
    assignments = []
    for twork in tworks:
      assignments.append([twork])
    works2 = Work.objects.filter(lesson_id=lesson, user_id=user_id, typing=1).order_by("-id")
    for work in works2:
        assignments[0].append(work.memo)
    return render(request, 'student/memo_user.html', {'works':works, 'lesson_list':lesson_list, 'assignments':assignments, 'student': user})

# 查詢某班級心得
def memo_all(request, classroom_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    classroom_name = Classroom.objects.get(id=classroom_id).name
    return render(request, 'student/memo_all.html', {'enrolls':enrolls, 'classroom_name':classroom_name})

# 查詢某班級心得統計
def memo_count(request, classroom_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    members = []
    for enroll in enrolls:
        members.append(enroll.student_id)
    classroom = Classroom.objects.get(id=classroom_id)
    works = Work.objects.filter(user_id__in=members, lesson_id=classroom.lesson)
    memo = ""
    for work in works:
        memo += work.memo
    memo = memo.rstrip('\r\n')
    seglist = jieba.cut(memo, cut_all=False)
    hash = {}
    for item in seglist:
        if item in hash:
            hash[item] += 1
        else:
            hash[item] = 1
    words = []
    count = 0
    error=""
    for key, value in sorted(hash.items(), key=lambda x: x[1], reverse=True):
        if ord(key[0]) > 32 :
            count += 1
            words.append([key, value])
            if count == 30:
                break
    return render(request, 'student/memo_count.html', {'total':works.count(), 'words':words, 'enrolls':enrolls, 'classroom':classroom})



# 查詢某班級某作業心得統計
def memo_work_count(request, classroom_id, work_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    members = []
    for enroll in enrolls:
        members.append(enroll.student_id)
    classroom = Classroom.objects.get(id=classroom_id)
    works = Work.objects.filter(user_id__in=members, index=int(work_id), lesson_id=classroom.lesson)
    memo = ""
    for work in works:
        memo += work.memo
    memo = memo.rstrip('\r\n')
    seglist = jieba.cut(memo, cut_all=False)
    hash = {}
    for item in seglist:
        if item in hash:
            hash[item] += 1
        else:
            hash[item] = 1
    words = []
    count = 0
    for key, value in sorted(hash.items(), key=lambda x: x[1], reverse=True):
        count += 1
        if ord(key[0]) > 32 :
            words.append([key, value])
            if count == 30:
                break
    return render(request, 'student/memo_work_count.html', {'words':words, 'enrolls':enrolls, 'classroom':classroom,  'work_id':work_id, 'lesson':lesson_list[int(work_id)-1][2]})


# 查詢某班某詞句心得
def memo_word(request, classroom_id, word):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    members = []
    for enroll in enrolls:
        members.append(enroll.student_id)
    classroom = Classroom.objects.get(id=classroom_id)
    works = Work.objects.filter(user_id__in=members, memo__contains=word, lesson_id=classroom.lesson).order_by('index')
    for work in works:
        work.memo = work.memo.replace(word, '<font color=red>'+word+'</font>')
    return render(request, 'student/memo_word.html', {'word':word, 'works':works, 'classroom':classroom})

# 查詢某班某作業某詞句心得
def memo_work_word(request, classroom_id, work_id, word):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    members = []
    for enroll in enrolls:
        members.append(enroll.student_id)
    classroom = Classroom.objects.get(id=classroom_id)
    works = Work.objects.filter(user_id__in=members, index=work_id, memo__contains=word)
    for work in works:
        work.memo = work.memo.replace(word, '<font color=red>'+word+'</font>')
    return render(request, 'student/memo_work_word.html', {'word':word, 'works':works, 'classroom':classroom, 'lesson':lesson_list[int(work_id)-1][2]})


# 查詢個人心得
def memo_show(request, user_id, unit,classroom_id, score):
    user_name = User.objects.get(id=user_id).first_name
    del lesson_list[:]
    reset()
    works = Work.objects.filter(user_id=user_id)
    for work in works:
        lesson_list[work.index-1].append(work.score)
        lesson_list[work.index-1].append(work.publication_date)
        if work.score > 0 :
            score_name = User.objects.get(id=work.scorer).first_name
            lesson_list[work.index-1].append(score_name)
        else :
            lesson_list[work.index-1].append("null")
        lesson_list[work.index-1].append(work.memo)
    c = 0
    for lesson in lesson_list:
        assistant = Assistant.objects.filter(student_id=user_id, lesson=c+1)
        if assistant.exists() :
            lesson.append("V")
        else :
            lesson.append("")
        c = c + 1
        #enroll_group = Enroll.objects.get(classroom_id=classroom_id, student_id=request.user.id).group
    user = User.objects.get(id=user_id)
    return render(request, 'student/memo_show.html', {'classroom_id': classroom_id, 'works':works, 'lesson_list':lesson_list, 'user_name': user_name, 'unit':unit, 'score':score})

# 列出所有討論主題
class ForumListView(ListView):
    model = SFWork
    context_object_name = 'works'
    template_name = 'student/forum_list.html'

    def get_queryset(self):
        queryset = []
        fclass_dict = dict(((fclass.forum_id, fclass) for fclass in FClass.objects.filter(classroom_id=self.kwargs['classroom_id'])))
        #fclasses = FClass.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        fworks = FWork.objects.filter(id__in=fclass_dict.keys()).order_by("-id")
        sfwork_pool = SFWork.objects.filter(student_id=self.request.user.id).order_by("-id")
        for fwork in fworks:
            sfworks = filter(lambda w: w.index==fwork.id, sfwork_pool)
            if len(sfworks)> 0 :
                queryset.append([fwork, sfworks[0].publish, fclass_dict[fwork.id], len(sfworks)])
            else :
                queryset.append([fwork, False, fclass_dict[fwork.id], 0])
        def getKey(custom):
            return custom[2].publication_date, custom[2].forum_id
        queryset = sorted(queryset, key=getKey, reverse=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ForumListView, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        context['bookmark'] =  self.kwargs['bookmark']
        context['fclasses'] = dict(((fclass.forum_id, fclass) for fclass in FClass.objects.filter(classroom_id=self.kwargs['classroom_id'])))
        return context

    # 限本班同學
    def render_to_response(self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(ForumListView, self).render_to_response(context)

# 發表心得
def forum_publish(request, classroom_id, index, action):
    if action == "1":
        try:
            fwork = FWork.objects.get(id=index)
            works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
            work = works[0]
            work.publish = True
            work.save()
            update_avatar(request.user.id, 3, 2)
            # History
            history = PointHistory(user_id=request.user.id, kind=1, message=u'2分--繳交討論區作業<'+fwork.title+'>', url='/student/forum/memo/'+classroom_id+'/'+index+'/'+action)
            history.save()
        except ObjectDoesNotExist:
            pass
        return redirect("/student/forum/memo/"+classroom_id+"/"+index+"/0")
    elif action == "0":
        return redirect("/student/forum/memo/"+classroom_id+"/"+index+"/0")
    else :
        return render(request, 'student/forum_publish.html', {'classroom_id': classroom_id, 'index': index})


def forum_submit(request, classroom_id, index):
    scores = []
    works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
    contents = FContent.objects.filter(forum_id=index).order_by("id")
    fwork = FWork.objects.get(id=index)
    if request.method == 'POST':
        form = ForumSubmitForm(request.POST, request.FILES)
        #第一次上傳加上積分
        works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
        work = SFWork(index=index, student_id=request.user.id, publish=False)
        work.save()
        if request.FILES:
            content = SFContent(index=index, student_id=request.user.id)
            myfile =  request.FILES.get("file", "")
            fs = FileSystemStorage()
            filename = uuid4().hex
            content.title = myfile.name
            content.work_id = work.id
            content.filename = str(request.user.id)+"/"+filename
            fs.save("static/upload/"+str(request.user.id)+"/"+filename, myfile)
            content.save()
        if form.is_valid():
            work.memo=form.cleaned_data['memo']
            work.memo_e = form.cleaned_data['memo_e']
            work.memo_c = form.cleaned_data['memo_c']
            work.save()
            if not works:
                return redirect("/student/forum/publish/"+classroom_id+"/"+index+"/2")
            elif not works[0].publish:
                return redirect("/student/forum/publish/"+classroom_id+"/"+index+"/2")
            return redirect("/student/forum/memo/"+classroom_id+"/"+index+"/0")
        else:
            return render_to_response('student/forum_form.html', {'error':form.errors}, context_instance=RequestContext(request))
    else:
        if not works.exists():
            work = SFWork(index=0, publish=False)
            form = ForumSubmitForm()
        else:
            work = works[0]
            form = ForumSubmitForm()
        files = SFContent.objects.filter(index=index, student_id=request.user.id,visible=True).order_by("-id")
        subject = FWork.objects.get(id=index).title
    return render(request, 'student/forum_form.html', {'classroom_id':classroom_id, 'subject':subject, 'files':files, 'index': index, 'fwork':fwork, 'works':works, 'work':work, 'form':form, 'scores':scores, 'index':index, 'contents':contents})

def forum_show(request, index, user_id, classroom_id):
    user = User.objects.get(id=user_id)
    if not (is_classmate(user, classroom_id) or is_teacher(request.user, classroom_id)) :
        return redirect("/")
    forum = FWork.objects.get(id=index)
    teacher_id = forum.teacher_id
    work = []
    replys = []
    files = []
    works = SFWork.objects.filter(index=index, student_id=user_id).order_by("-id")
    contents = FContent.objects.filter(forum_id=index).order_by("id")
    publish = False
    if len(works)> 0:
        work_new = works[0]
        work_first = works.last()
        publish = work_first.publish
        replys = SFReply.objects.filter(index=index, work_id=work_first.id).order_by("-id")
        files = SFContent.objects.filter(index=index, student_id=user_id, visible=True).order_by("-id")
    else :
        work_new = SFWork(index=index, student_id=user_id)
        work_first = SFWork(index=index, student_id=user_id)
    return render(request, 'student/forum_show.html', {'work_new': work_new, 'work_first':work_first, 'publish':publish, 'classroom_id':classroom_id, 'contents':contents, 'replys':replys, 'files':files, 'forum':forum, 'user_id':user_id, 'teacher_id':teacher_id, 'works': works, 'is_teacher':is_teacher(request.user, classroom_id)})

 # 查詢某作業所有同學心得
def forum_memo(request, classroom_id, index, action):
	if not is_classmate(request.user, classroom_id):
		return redirect("/")
	enrolls = Enroll.objects.filter(classroom_id=classroom_id)
	datas = []
	contents = FContent.objects.filter(forum_id=index).order_by("-id")
	fwork = FWork.objects.get(id=index)
	teacher_id = fwork.teacher_id
	subject = fwork.title
	if action == "2":
		works_pool = SFWork.objects.filter(index=index, score=5).order_by("-id")
	else:
	  # 一次取得所有 SFWork
	  works_pool = SFWork.objects.filter(index=index).order_by("-id", "publish")
	reply_pool = SFReply.objects.filter(index=index).order_by("-id")
	file_pool = SFContent.objects.filter(index=index, visible=True).order_by("-id")
	for enroll in enrolls:
		works = filter(lambda w: w.student_id==enroll.student_id, works_pool)
		# 對未作答學生不特別處理，因為 filter 會傳回 []
		if len(works)>0:
			replys = filter(lambda w: w.work_id==works[-1].id, reply_pool)
			files = filter(lambda w: w.student_id==enroll.student_id, file_pool)
			if action == "2" :
			  if works[-1].score == 5:
					datas.append([enroll, works, replys, files])
			else :
				datas.append([enroll, works, replys, files])
		else :
			replys = []
			if not action == "2" :
				files = filter(lambda w: w.student_id==enroll.student_id, file_pool)
				datas.append([enroll, works, replys, files])
	def getKey(custom):
		if custom[1]:
			if action == "3":
				return custom[1][-1].like_count
			elif action == "2":
				return custom[1][-1].score, custom[1][0].publication_date
			elif action == "1":
				return -custom[0].seat
			else :
				return custom[1][0].reply_date, -custom[0].seat
		else:
			return -custom[0].seat
	datas = sorted(datas, key=getKey, reverse=True)

	return render(request, 'student/forum_memo.html', {'action':action, 'replys':replys, 'datas': datas, 'contents':contents, 'teacher_id':teacher_id, 'subject':subject, 'classroom_id':classroom_id, 'index':index, 'is_teacher':is_teacher(request.user, classroom_id)})

def forum_history(request, user_id, index, classroom_id):
    work = []
    contents = FContent.objects.filter(forum_id=index).order_by("-id")
    works = SFWork.objects.filter(index=index, student_id=user_id).order_by("-id")
    files = SFContent.objects.filter(index=index, student_id=user_id).order_by("-id")
    forum = FWork.objects.get(id=index)
    if len(works)> 0 :
        if works[0].publish or user_id==str(request.user.id) or is_teacher(request.user, classroom_id):
            return render(reuqest, 'student/forum_history.html', {'forum': forum, 'classroom_id':classroom_id, 'works':works, 'contents':contents, 'files':files, 'index':index})
    return redirect("/")

def forum_like(request):
    forum_id = request.POST.get('forumid')
    classroom_id = request.POST.get('classroomid')
    user_id = request.POST.get('userid')
    action = request.POST.get('action')
    likes = []
    sfworks = []
    fwork = FWork.objects.get(id=forum_id)
    user = User.objects.get(id=user_id)
    if forum_id:
        try:
            sfworks = SFWork.objects.filter(index=forum_id, student_id=user_id)
            sfwork = sfworks[0]
            jsonDec = json.decoder.JSONDecoder()
            if action == "like":
                if sfwork.likes:
                    likes = jsonDec.decode(sfwork.likes)
                    if not request.user.id in likes:
                        likes.append(request.user.id)
                else:
                    likes.append(request.user.id)
                sfwork.likes = json.dumps(likes)
                sfwork.like_count = len(likes)
                sfwork.save()
                update_avatar(request.user.id, 3, 0.1)
                # History
                history = PointHistory(user_id=request.user.id, kind=3, message=u'+0.1分--討論區按讚<'+fwork.title+'><'+user.first_name+'>', url="/student/forum/memo/"+classroom_id+"/"+forum_id+"/0/#"+user_id)
                history.save()
            else:
                if sfwork.likes:
                    likes = jsonDec.decode(sfwork.likes)
                    if request.user.id in likes:
                        likes.remove(request.user.id)
                        sfwork.likes = json.dumps(likes)
                        sfwork.like_count = len(likes)
                        sfwork.save()
                        #積分
                        update_avatar(request.user.id, 3, -0.1)
                        # History
                        history = PointHistory(user_id=request.user.id, kind=3, message=u'-0.1分--討論區按讚取消<'+fwork.title+'><'+user.first_name+'>', url="/student/forum/memo/"+classroom_id+"/"+forum_id+"/0/#"+user_id)
                        history.save()
        except ObjectDoesNotExist:
            sfworks = []

        return JsonResponse({'status':'ok', 'likes':sfworks[0].likes}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)

def forum_reply(request):
    forum_id = request.POST.get('forumid')
    classroom_id = request.POST.get('classroomid')
    user_id = request.POST.get('userid')
    work_id = request.POST.get('workid')
    text = request.POST.get('reply')
    fwork = FWork.objects.get(id=forum_id)
    user = User.objects.get(id=user_id)
    if forum_id:
        reply = SFReply(index=forum_id, work_id=work_id, user_id=user_id, memo=text, publication_date=timezone.now())
        reply.save()
        sfwork = SFWork.objects.get(id=work_id)
        sfwork.reply_date = timezone.now()
        sfwork.save()
        update_avatar(request.user.id, 3, 0.2)
        # History
        history = PointHistory(user_id=request.user.id, kind=3, message=u'0.2分--討論區留言<'+fwork.title+'><'+user.first_name+'>', url='/student/forum/memo/'+classroom_id+'/'+forum_id+'/0/#'+user_id)
        history.save()

        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)


def forum_guestbook(request):
    work_id = request.POST.get('workid')
    guestbooks = "<table class=table>"
    if work_id:
        try :
            replys = SFReply.objects.filter(work_id=work_id).order_by("-id")
        except ObjectDoesNotExist:
            replys = []
        for reply in replys:
            user = User.objects.get(id=reply.user_id)
            guestbooks += '<tr><td nowrap>' + user.first_name + '</td><td>' + reply.memo + "</td></tr>"
        guestbooks += '</table>'
        return JsonResponse({'status':'ok', 'replys': guestbooks}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)

def forum_people(request):
    forum_id = request.POST.get('forumid')
    user_id = request.POST.get('userid')
    likes = []
    sfworks = []
    names = []
    if forum_id:
        try:
            sfworks = SFWork.objects.filter(index=forum_id, student_id=user_id).order_by("id")
            sfwork = sfworks[0]
            jsonDec = json.decoder.JSONDecoder()
            if sfwork.likes:
                likes = jsonDec.decode(sfwork.likes)
                for like in reversed(likes):
                  user = User.objects.get(id=like)
                  names.append('<button type="button" class="btn btn-default">'+user.first_name+'</button>')
        except ObjectDoesNotExist:
            sfworks = []
        return JsonResponse({'status':'ok', 'likes':names}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)

def forum_score(request):
    work_id = request.POST.get('workid')
    classroom_id = request.POST.get('classroomid')
    user_id = request.POST.get('userid')
    score = request.POST.get('score')
    comment = request.POST.get('comment')
    if work_id and is_teacher(request.user, classroom_id):
        sfwork = SFWork.objects.get(id=work_id)
        sfwork.score = score
        sfwork.comment = comment
        sfwork.scorer = request.user.id
        sfwork.comment_publication_date = timezone.now()
        sfwork.save()
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)

# 統計某討論主題所有同學心得
def forum_jieba(request, classroom_id, index):
    classroom = Classroom.objects.get(id=classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    works = []
    contents = FContent.objects.filter(forum_id=index).order_by("-id")
    fwork = FWork.objects.get(id=index)
    teacher_id = fwork.teacher_id
    subject = fwork.title
    memo = ""
    for enroll in enrolls:
        try:
            works = SFWork.objects.filter(index=index, student_id=enroll.student_id).order_by("-id")
            if works:
                memo += works[0].memo
        except ObjectDoesNotExist:
            pass
    memo = memo.rstrip('\r\n')
    seglist = jieba.cut(memo, cut_all=False)
    hash = {}
    for item in seglist:
        if item in hash:
            hash[item] += 1
        else:
            hash[item] = 1
    words = []
    count = 0
    error=""
    for key, value in sorted(hash.items(), key=lambda x: x[1], reverse=True):
        if ord(key[0]) > 32 :
            count += 1
            words.append([key, value])
            if count == 100:
                break
    return render(request, 'student/forum_jieba.html', {'index': index, 'words':words, 'enrolls':enrolls, 'classroom':classroom, 'subject':subject})

# 查詢某班某詞句心得
def forum_word(request, classroom_id, index, word):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    work_ids = []
    datas = []
    pos = word.index(' ')
    word = word[0:pos]
    for enroll in enrolls:
        try:
            works = SFWork.objects.filter(index=index, student_id=enroll.student_id,memo__contains=word).order_by("-id")
            if works:
                work_ids.append(works[0].id)
                datas.append([works[0], enroll.seat])
        except ObjectDoesNotExist:
            pass
    classroom = Classroom.objects.get(id=classroom_id)
    for work, seat in datas:
        work.memo = work.memo.replace(word, '<font color=red>'+word+'</font>')
    return render(request, 'student/forum_word.html', {'word':word, 'datas':datas, 'classroom':classroom})

# 下載檔案
def forum_download(request, file_id):
    content = SFContent.objects.get(id=file_id)
    filename = content.title
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    download =  BASE_DIR + "/static/upload/" + content.filename
    wrapper = FileWrapper(file( download, "r" ))
    response = HttpResponse(wrapper, content_type = 'application/force-download')
    #response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename.encode('utf8'))
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response

# 顯示圖片
def forum_showpic(request, file_id):
    content = SFContent.objects.get(id=file_id)
    return render(request, 'student/forum_showpic.html', {'content':content})

# ajax刪除檔案
def forum_file_delete(request):
    file_id = request.POST.get('fileid')
    if file_id:
        try:
            file = SFContent.objects.get(id=file_id)
            file.visible = False
            file.delete_date = timezone.now()
            file.save()
        except ObjectDoesNotExist:
            file = []
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)

def content_delete(request, types, typing, lesson, index, content_id):
  if types == "11" or types == "12":
    instance = Science1Content.objects.get(id=content_id)
    instance.delete()

    return redirect("/student/work/submit/"+typing+"/"+lesson+"/"+index+"/#tab1")
  elif types == "41" or types== "42":
    instance = Science4Content.objects.get(id=content_id)
    instance.delete()

    return redirect("/student/work/submit/"+typing+"/"+lesson+"/"+index+"/#tab4")

def content_edit(request, types, typing, lesson, index, content_id):
    try:
        if types == "11" or types == "12":
            instance = Science1Content.objects.get(id=content_id)
        elif types == "41" or types== "42":
            instance = Science4Content.objects.get(id=content_id)
    except:
        pass
    if request.method == 'POST':
            content_id = request.POST.get("content_id")
            if types == "11" or types == "12":
                try:
                    content = Science1Content.objects.get(id=content_id)
                except ObjectDoesNotExist:
	                  content = Science1Content(types= request.POST.get("types"))
            elif types == "41" or types== "42":
                try:
                    content = Science4Content.objects.get(id=content_id)
                except ObjectDoesNotExist:
	                  content = Science4Content(types= request.POST.get("types"))
            if content.types == 11 or content.types == 41:
                content.text = request.POST.get("text")
            elif content.types == 12 or content.types == 42:
                myfile =  request.FILES.get("content_file")
                fs = FileSystemStorage()
                filename = uuid4().hex
                content.picname = str(request.user.id)+"/"+filename
                fs.save("static/upload/"+str(request.user.id)+"/"+filename, myfile)
            content.save()
            if types == "11" or types == "12":
                return redirect("/student/work/submit/"+typing+"/"+lesson+"/"+index+"/#tab1")
            elif types == "41" or types== "42":
                return redirect("/student/work/submit/"+typing+"/"+lesson+"/"+index+"/#tab4")
    return render(request,'student/work_content_edit.html',{'content': instance, 'content_id':content_id, 'types':types, 'typing':typing, 'lesson':lesson, 'index':index})