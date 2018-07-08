# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
#from django.contrib.auth import authenticate, login
from django.template import RequestContext
from student.lesson import *
from django.views.generic import ListView, CreateView
from student.models import Enroll, EnrollGroup, WorkAssistant, Work, WorkFile, Answer, Exam
from teacher.models import Classroom, TWork
from show.models import Round
from account.models import Message, MessagePoll, Profile, VisitorLog, PointHistory, LessonCounter, DayCounter, LogCounter
from account.avatar import *
from student.forms import EnrollForm, GroupForm, SeatForm, GroupSizeForm, SubmitAForm, SubmitBForm
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
    return render_to_response('student/lessons.html', {'subject_id': subject_id, 'counter': hit, 'lock':lock}, context_instance=RequestContext(request))

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
        return render_to_response('student/lessonA.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':0 }, context_instance=RequestContext(request))
    elif lesson[0] == "B":
        lesson_id = 2
        profile_lock = profile.lock2
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(typing=0, lesson_id=lesson_id, user_id=request.user.id)))
        # 限登入者
        if not request.user.is_authenticated():
            return redirect("/account/login/")
        else :
            lock = {'B02':3, 'B03':4, 'B04':5, 'B05':6, 'B06':7, 'B07':8, 'B08':9, 'B09':10, 'B10':11, 'B11':12, 'B12':13, 'B13':14, 'B14':15, 'B15':16, 'B16':17, 'B17':17, 'B18':17}
        if lesson in lock:
            if profile_lock < lock[lesson]:
                if not request.user.groups.filter(name='teacher').exists():
                    return redirect("/")

        return render_to_response('student/lessonB.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':0}, context_instance=RequestContext(request))
    elif lesson[0] == "C":
        lesson_id = 3
        profile_lock = profile.lock3
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(lesson_id=lesson_id, user_id=request.user.id)))
        return render_to_response('student/lessonC.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':0}, context_instance=RequestContext(request))
    elif lesson[0] == "D":
        lesson_id = 4
        profile_lock = profile.lock4
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(lesson_id=lesson_id, user_id=request.user.id)))
        return render_to_response('student/lessonD.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':0}, context_instance=RequestContext(request))
    elif lesson[0] == "E":
        lesson_id = 5
        profile_lock = profile.lock5
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(typing=0, lesson_id=lesson_id, user_id=request.user.id)))
        # 限登入者
        if not request.user.is_authenticated():
            return redirect("/account/login/")
        else :
            lock = {'E02':3, 'E03':4, 'E04':5, 'E05':6, 'E06':7, 'E07':8, 'E08':9, 'E09':10, 'E10':11, 'E11':12, 'E12':13, 'E13':14, 'E14':15, 'E15':16, 'E16':17, 'E17':17, 'E18':17}
        if lesson in lock:
            if profile_lock < lock[lesson]:
                if not request.user.groups.filter(name='teacher').exists():
                    return redirect("/")

        return render_to_response('student/lessonE.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':0}, context_instance=RequestContext(request))
    else:
        lesson_id = 1
        profile_lock = profile.lock1
        work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(lesson_id=lesson_id, user_id=request.user.id)))
        return render_to_response('student/lessonA.html', {'lesson': lesson, 'lesson_id': lesson_id, 'work_dict': work_dict, 'counter':hit, 'typing':0}, context_instance=RequestContext(request))

# 判斷是否為授課教師
def is_teacher(user, classroom_id):
    return  user.groups.filter(name='teacher').exists() and Classroom.objects.filter(teacher_id=user.id, id=classroom_id).exists()

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

        return render_to_response('student/classmate.html', {'classroom':classroom, 'enrolls':enroll_group}, context_instance=RequestContext(request))

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

        #找出尚未分組的學生
        def getKey(custom):
            return custom.seat
        enrolls = Enroll.objects.filter(classroom_id=classroom_id)
        nogroup = []
        for enroll in enrolls:
            if enroll.group == 0 :
		        nogroup.append(enroll)
	    nogroup = sorted(nogroup, key=getKey)

        return render_to_response('student/group.html', {'nogroup': nogroup, 'group_open': group_open, 'student_groups':student_groups, 'classroom':classroom, 'student_group':student_group, 'teacher': is_teacher(request.user, classroom_id)}, context_instance=RequestContext(request))

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
        return render_to_response('form.html', {'form':form}, context_instance=RequestContext(request))

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
        return render_to_response('form.html', {'form':form}, context_instance=RequestContext(request))

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
def classroom(request):
        classrooms = []
        enrolls = Enroll.objects.filter(student_id=request.user.id).order_by("-id")
        round_pool = Round.objects.all().order_by("-id")
        for enroll in enrolls :
            shows = filter(lambda w: w.classroom_id == enroll.classroom_id, round_pool)
            classrooms.append([enroll, shows])
        return render_to_response('student/classroom.html',{'classrooms':classrooms}, context_instance=RequestContext(request))

# 查看可加入的班級
def classroom_add(request):
        classrooms = Classroom.objects.all().order_by('-id')
        classroom_teachers = []
        for classroom in classrooms:
            enroll = Enroll.objects.filter(student_id=request.user.id, classroom_id=classroom.id)
            if enroll.exists():
                classroom_teachers.append([classroom,classroom.teacher.first_name,1])
            else:
                classroom_teachers.append([classroom,classroom.teacher.first_name,0])

        return render_to_response('student/classroom_add.html', {'classroom_teachers':classroom_teachers}, context_instance=RequestContext(request))

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
                        return render_to_response('message.html', {'message':"選課密碼錯誤"}, context_instance=RequestContext(request))
                except Classroom.DoesNotExist:
                    pass
                return redirect("/student/group/" + str(classroom.id))
        else:
            form = EnrollForm()
        return render_to_response('form.html', {'form':form}, context_instance=RequestContext(request))

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

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))

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
    def render_to_response(self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(AnnounceListView, self).render_to_response(context)

# 列出個人所有作業
def work_list(request, typing, lesson, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    lessons = []

    if typing == "0":
        if lesson in ["2", "3", "4", "5"]:
            assignments = [lesson_list2, lesson_list3, lesson_list4, lesson_list2][int(lesson)-2]
        else:
            assignments = lesson_list1
    elif typing == "1":
        assignments = TWork.objects.filter(classroom_id=classroom_id).order_by("-id")
    work_dict = dict(((work.index, work) for work in Work.objects.filter(typing=typing, user_id=request.user.id, lesson_id=lesson)))

    for idx, assignment in enumerate(assignments):
        if typing == "0":
            index = idx+1
        elif typing == "1":
            index = assignment.id
        if not index in work_dict:
            lessons.append([assignment, None])
        else:
           lessons.append([assignment, work_dict[index]])
    return render_to_response('student/work_list.html', {'typing':typing, 'lesson':lesson, 'lessons':lessons, 'classroom':classroom}, context_instance=RequestContext(request))

def submit(request, typing, lesson, index):
    work_dict = {}
    form = None
    work_dict = dict(((int(work.index), [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(typing=typing, lesson_id=lesson, user_id=request.user.id)))
    if typing == "0":
        if lesson in ["2", "3", "4", "5"]:
            lesson_name = [lesson_list2, lesson_list3, lesson_list4, lesson_list2][int(lesson)-2][int(index)-1][1]
        else:
            lesson_name = lesson_list1[int(index)-1][2]
    elif typing == "1":
        lesson_name = TWork.objects.get(id=index).title

    if lesson == "1":
        works = Work.objects.filter(typing=typing, index=index, user_id=request.user.id, lesson_id=lesson)
        try:
            filepath = request.FILES['file']
        except :
            filepath = False
        if request.method == 'POST':
            if filepath :
                myfile = request.FILES['file']
                fs = FileSystemStorage()
                filename = uuid4().hex
                fs.save("static/work/scratch/"+str(request.user.id)+"/"+filename, myfile)
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
                    works.update(memo=form.cleaned_data['memo'],publication_date=timezone.localtime(timezone.now()))
                    workfile = WorkFile(work_id=works[0].id, filename=filename)
                    workfile.save()
                else :
                    works.update(memo=form.cleaned_data['memo'])
            return redirect("/student/work/show/"+typing+"/"+lesson+"/"+index+"/"+str(request.user.id))
    elif lesson == "2" or lesson == "3" or lesson == "4" or lesson == "5":
        if request.method == 'POST':
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
                        elif lesson == "4":
                            profile.lock4 +=1
                        elif lesson == "5":
                            profile.lock5 +=1                            
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

                    prefix = ['static/work/vphysics', 'static/work/euler', 'static/work/ck', 'static/work/vphysics2'][int(lesson) - 2]
                    directory = "{prefix}/{uid}/{index}".format(prefix=prefix, uid=request.user.id, index=index)
                    image_file = "{path}/{id}.jpg".format(path=directory, id=work.id)

                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    with open(image_file, 'wb') as fd:
                        fd.write(binary_data)
                        fd.close()
                    work.picture=image_file
                except ValueError:
                    path = dataURI.split('/', 3)
                    work.picture=path[3]
                    pass
                work.code=form.cleaned_data['code']
                work.memo=form.cleaned_data['memo']
                work.helps=form.cleaned_data['helps']
                work.save()
                return redirect("/student/work/show/"+typing+"/"+lesson+"/"+index+"/"+str(request.user.id))
            return redirect('/student/lesson/'+request.POST.get("lesson", ""))
    return render_to_response('student/submit.html', {'form':form, 'typing':typing, 'lesson':lesson, 'index':index, 'work_dict':work_dict}, context_instance=RequestContext(request))

def show(request, typing, lesson, index, user_id):
    work_dict = dict(((work.index, [work, WorkFile.objects.filter(work_id=work.id).order_by("-id")]) for work in Work.objects.filter(typing=typing, lesson_id=lesson, user_id=request.user.id)))
    if int(user_id) == request.user.id or request.user.is_superuser:
        try:
            work = Work.objects.get(typing=typing, lesson_id=lesson, index=index, user_id=user_id)
        except ObjectDoesNotExist:
            work = None
        except MultipleObjectsReturned:
            work = Work.objects.filter(typing=typing, lesson_id=lesson, index=index, user_id=user_id).last()
        return render_to_response('student/show.html', {'work':work, 'lesson':lesson, 'work_dict':work_dict, 'index':index}, context_instance=RequestContext(request))
    else :
        return redirect("/")

def rank(request, typing, lesson, index):
    works = Work.objects.filter(typing=typing, lesson_id=lesson, index=index).order_by("id")
    return render_to_response('student/rank.html', {'works':works, 'lesson':lesson}, context_instance=RequestContext(request))

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

    return render_to_response('student/memo.html', {'datas': datas}, context_instance=RequestContext(request))

def work_download(request, index, user_id, workfile_id):
    workfile = WorkFile.objects.get(id=workfile_id)
    username = User.objects.get(id=user_id).first_name
    filename = username + "_" + lesson_list1[int(index)-1][2].decode("utf-8")  + ".sb2"
    download =  settings.BASE_DIR + "/static/work/scratch/" + str(user_id) + "/" + workfile.filename
    wrapper = FileWrapper(file( download, "r" ))
    response = HttpResponse(wrapper, content_type = 'application/force-download')
    #response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename.encode('utf8'))
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
    #return render_to_response('student/download.html', {'download':download})

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
                  index = 17
              elif unit == "3":
                  lesson_list = lesson_list1[25:33]
                  index = 25
              elif unit == "4":
                  lesson_list = lesson_list1[33:41]
                  index = 33
              else:
                  lesson_list = lesson_list1[0:17]
          elif lesson == "2":
              lesson_list = lesson_list2
          elif lesson == "3":
              lesson_list = lesson_list3
          elif lesson == "4":
              lesson_list = lesson_list4
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
    return render_to_response('student/progress.html', {'typing':typing, 'lesson':lesson, 'unit':unit, 'bars':bars,'classroom':classroom, 'lesson_list':lesson_list}, context_instance=RequestContext(request))

# 查詢某作業分組小老師
def work_group(request, typing, lesson, index, classroom_id):
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
        student_groups = []
        lesson = Classroom.objects.get(id=classroom_id).lesson
        groups = EnrollGroup.objects.filter(classroom_id=classroom_id)
        try:
                student_group = Enroll.objects.get(student_id=request.user.id, classroom_id=classroom_id).group
        except ObjectDoesNotExist :
                student_group = []
        for group in groups:
            enrolls = Enroll.objects.filter(classroom_id=classroom_id, group=group.id)
            group_assistants = []
            works = []
            scorer_name = ""
            for enroll in enrolls:
                try:
                    work = Work.objects.get(user_id=enroll.student_id, index=index, lesson_id=lesson)
                    if work.scorer > 0 :
                        scorer = User.objects.get(id=work.scorer)
                        scorer_name = scorer.first_name
                    else :
                        scorer_name = "X"
                except ObjectDoesNotExist:
                    work = Work(lesson_id=lesson, index=index, user_id=1, score=-2)
                except MultipleObjectsReturned:
                    work = Work.objects.filter(user_id=enroll.student_id, index=index, lesson_id=lesson).order_by("-id")[0]
                works.append([enroll, work.score, scorer_name, work.file])
                try :
                    assistant = WorkAssistant.objects.get(typing=typing, student_id=enroll.student.id, classroom_id=classroom_id, lesson_id=lesson, index=index)
                    group_assistants.append(enroll)
                except ObjectDoesNotExist:
                    pass
            student_groups.append([group, works, group_assistants])
        lesson_dict = {}
        c = 0
        for assignment in lesson_list:
            c = c + 1
            lesson_dict[c] = assignment[0]
        assignment = lesson_dict[int(index)]
        return render_to_response('student/work_group.html', {'lesson':lesson, 'assignment':assignment, 'student_groups':student_groups, 'classroom_id':classroom_id}, context_instance=RequestContext(request))

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
    return render_to_response('student/answer.html', {'lesson':lesson, 'index':index, 'answer':answer, 'work':work}, context_instance=RequestContext(request))

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
        return render_to_response('student/exam.html', context_instance=RequestContext(request))

# 測驗卷得分
def exam_score(request):
    exams = Exam.objects.filter(student_id=request.user.id)
    return render_to_response('student/exam_score.html', {'exams':exams} , context_instance=RequestContext(request))

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
    exam = Exam(exam_id=int(exam_id)+1, student_id=request.user.id, answer=ua_test, score=score)
    exam.save()
    return JsonResponse({'status':'ok','answer':answer}, safe=False)