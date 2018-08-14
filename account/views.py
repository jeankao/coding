# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forms import LoginForm, RegistrationForm, RegistrationSchoolForm, PasswordForm, RealnameForm, LineForm, SchoolForm, EmailForm, LoginStudentForm, TeacherApplyForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView
from django.db.models import Q
from zone import *
from account.models import County, Zone, School, Profile, PointHistory, Message, MessageContent, MessagePoll, Visitor, VisitorLog, LessonCounter
from student.models import Work
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.timezone import localtime
from student.models import Enroll
from certificate.models import Certificate
from django.apps import apps
from teacher.models import Classroom
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from django.conf import settings
from wsgiref.util import FileWrapper
from django.http import HttpResponse

# 判斷是否為任教學生
def is_student(user_id, request):
    classrooms = Classroom.objects.filter(teacher_id=request.user.id)
    for classroom in classrooms:
        if Enroll.objects.filter(classroom_id=classroom.id, student_id=user_id).exists(): 
            return True
    return False
    
# 判斷是否為本班同學
def is_classmate(user_id, classroom_id):
    return Enroll.objects.filter(student_id=user_id, classroom_id=classroom_id).exists()
      
# 網站首頁
def homepage(request):
    models = apps.get_models()
    row_count = 0
    for model in models:
        row_count = row_count + model.objects.count()
    users = User.objects.all()
    try :
        admin_user = User.objects.get(id=1)
        admin_profile = Profile.objects.get(user=admin_user)
        admin_profile.home_count = admin_profile.home_count + 1
        admin_profile.save()
    except ObjectDoesNotExist:
        admin_profile = ""
    classroom_count = Classroom.objects.all().count()
        
    teacher = User.objects.filter(groups__name='teacher').count()
    student = Enroll.objects.values('student_id').distinct().count()
    workss = Work.objects.all()
    classrooms = Classroom.objects.all()
    class_scratch_pool = [classroom for classroom in filter(lambda w: w.lesson == 1, classrooms)]    
    class_scratch_ids = map(lambda a: a.id, class_scratch_pool)    
    class_scratch = len(class_scratch_pool)    
    class_vphysics_pool = [classroom for classroom in filter(lambda w: w.lesson == 2 or w.lesson == 4, classrooms)]    
    class_vphysics_ids = map(lambda a: a.id, class_vphysics_pool)    
    class_vphysics = len(class_vphysics_pool)    
    class_euler_pool = [classroom for classroom in filter(lambda w: w.lesson == 3, classrooms)]    
    class_euler_ids = map(lambda a: a.id, class_euler_pool)    
    class_euler = len(class_euler_pool)      
    work_scratch = len(filter(lambda w: w.lesson_id == 1, workss))
    work_vphysics = len(filter((lambda w: w.lesson_id == 2 or w.lesson_id == 4), workss))
    work_euler = len(filter(lambda w: w.lesson_id == 3, workss))
    works = [len(workss), [class_scratch, work_scratch], [class_vphysics, work_vphysics], [class_euler, work_euler]]
    enrolls = Enroll.objects.filter(seat__gt=0)
    certificate_scratch1 = len(filter(lambda w: w.certificate1 == True, enrolls))
    certificate_scratch2 = len(filter(lambda w: w.certificate2 == True, enrolls))
    certificate_scratch3 = len(filter(lambda w: w.certificate3 == True, enrolls))
    certificate_scratch4 = len(filter(lambda w: w.certificate4 == True, enrolls))
    certificate_scratch = certificate_scratch1+certificate_scratch2+certificate_scratch3+certificate_scratch4
    certificate_vphysics =  len(filter(lambda w: w.certificate_vphysics == True, enrolls))
    certificate_euler =  len(filter(lambda w: w.certificate_euler == True, enrolls))
    classroom_scratch = [enroll for enroll in enrolls if enroll.classroom_id in class_scratch_ids]
    enroll_scratch =  len(filter(lambda w: w.classroom_id, classroom_scratch))
    classroom_vphysics = [enroll for enroll in enrolls if enroll.classroom_id in class_vphysics_ids]
    enroll_vphysics =  len(filter(lambda w: w.classroom_id, classroom_vphysics))    
    classroom_euler = [enroll for enroll in enrolls if enroll.classroom_id in class_euler_ids]
    enroll_euler =  len(filter(lambda w: w.classroom_id, classroom_euler))
    certificate = certificate_scratch+certificate_vphysics+certificate_euler
    certificates = [certificate, [enroll_scratch, certificate_scratch], [enroll_vphysics, certificate_vphysics], [enroll_euler, certificate_euler]]
    return render_to_response('homepage.html', {'certificates':certificates, 'works':works, 'teacher':teacher, 'student':student, 'classroom_count':classroom_count, 'row_count':row_count, 'user_count':len(users), 'admin_profile': admin_profile}, context_instance=RequestContext(request))
  
# 網站大廳
def dashboard(request):
    return render_to_response('account/dashboard.html', context_instance=RequestContext(request))
  
def author(request):   
    return render_to_response('account/author.html', context_instance=RequestContext(request))	
    
def about(request):   
    return render_to_response('account/about.html', context_instance=RequestContext(request))	  

def contact(request):   
    return render_to_response('account/contact.html', context_instance=RequestContext(request))	  	
    
def statics_zone(request):
    cities = County.objects.all()
    return render_to_response('account/statics_zone.html', {'cities':cities}, context_instance=RequestContext(request))	  	

def statics_lesson(request):
    counters = LessonCounter.objects.all().order_by("-hit")		
    return render_to_response('account/statics_lesson.html', {'counters':counters}, context_instance=RequestContext(request))
    
# 管理介面 
def admin(request):
    return render_to_response('account/admin.html', context_instance=RequestContext(request))
    
# 使用者登入功能
def user_login(request, role):
    message = None
    test = ""
    if request.method == "POST":
        if role == "0":
            form = LoginForm(request.POST)
        else:
            form = LoginStudentForm(request.POST)
        if form.is_valid():
            teacher = request.POST['teacher']					
            username = request.POST['username']
            password = request.POST['password']
            if role == "0":
                user = authenticate(username=username, password=password)
            else:
                user = authenticate(username=teacher+"_"+username, password=password)
            if user is not None:
                if user.is_active:
                    if user.id == 1:
                        zones = Zone.objects.all()
                        if len(zones) == 0:
                            for city_name, zones, mapx, mapy in county:
                                city = County(name=city_name, mapx=mapx, mapy=mapy)
                                city.save()
                                for zone_name in zones:
                                    zone = Zone(name=zone_name, county=city.id)
                                    zone.save()
                            school = School(county=1, zone=9, system=3, name="南港高中")
                            school.save()
                            user.last_name = "1"
                            user.save()
                        if user.first_name == "":
                            user.first_name = "管理員"                            
                            user.save()
                            try :
                                group = Group.objects.get(name="apply")	
                            except ObjectDoesNotExist :
                                group = Group(name="apply")
                                group.save()                                         
                            group.user_set.add(user)														
                            # create Message
                            title = "請修改您的姓名"
                            url = "/account/realname"
                            message = Message(title=title, url=url, time=timezone.now())
                            message.save()                        
                    
                            # message for group member
                            messagepoll = MessagePoll(message_id = message.id,reader_id=1)
                            messagepoll.save() 														
                    # 記錄訪客資訊
                    admin_user = User.objects.get(id=1)
                    try:
                        profile = Profile.objects.get(user=admin_user)
                    except ObjectDoesNotExist:
                        profile = Profile(user=admin_user)
                        profile.save()
                    profile.visitor_count = profile.visitor_count + 1
                    profile.save()
                                    
                    year = localtime(timezone.now()).year
                    month =  localtime(timezone.now()).month
                    day =  localtime(timezone.now()).day
                    date_number = year * 10000 + month*100 + day
                    try:
                        visitor = Visitor.objects.get(date=date_number)
                    except ObjectDoesNotExist:
                        visitor = Visitor(date=date_number)
                    visitor.count = visitor.count + 1
                    visitor.save()
                                        
                    visitorlog = VisitorLog(visitor_id=visitor.id, user_id=user.id, IP=request.META.get('REMOTE_ADDR'))
                    visitorlog.save()
                    # 登入成功，導到大廳
                    login(request, user)                                  
                    return redirect('/account/dashboard/0')                                        
                else:
                    message = "帳號未啟用!"
            else:
                message = "無效的帳號或密碼!"
    else:
        if role == "0":
            form = LoginForm()
        else:
            form = LoginStudentForm()
    return render_to_response('registration/login.html', {'role':role, 'message': message, 'form': form}, context_instance=RequestContext(request))

# 註冊帳號
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            try :
                group = Group.objects.get(name="apply")	
            except ObjectDoesNotExist :
                group = Group(name="apply")
                group.save()                                         
            group.user_set.add(new_user)													
            
            profile = Profile(user=new_user)
            profile.save()
            
            # create Message
            title = "申請成為教師以進行開班授課"
            url = "/account/teacher/apply"
            message = Message(title=title, url=url, time=timezone.now())
            message.save()                        
        
            # message for member
            messagepoll = MessagePoll(message_id = message.id,reader_id=new_user.id)
            messagepoll.save() 	      						
                        
            return render_to_response('registration/register_done.html',{'new_user': new_user}, context_instance=RequestContext(request))
    else:
        form = RegistrationForm()
    school_pool = School.objects.filter(online=True)
    return render_to_response('registration/register.html', {'form': form, 'schools': school_pool}, context_instance=RequestContext(request))

# 註冊學校
def register_school(request):      
    if request.method == 'POST':
        form = RegistrationSchoolForm(request.POST)    
        if form.is_valid():
            school = form.save()
            return redirect("/account/register?school="+str(school.county)+"/"+str(school.zone)+"/"+str(school.id))
    else:
        form = RegistrationSchoolForm()
    school_pool = School.objects.filter(online=True)
    return render_to_response('registration/register_school.html', {'form': form, 'schools': school_pool}, context_instance=RequestContext(request))
  
# 申請教師
def teacher_apply(request):      
    if request.method == 'POST':
        form = TeacherApplyForm(request.POST)    
        if form.is_valid():
            form.save()
            return redirect("/account/register")
    else:
        form = TeacherApplyForm()
    return render_to_response('account/teacher_apply.html', {'form': form}, context_instance=RequestContext(request))

# 超級管理員可以查看所有帳號
class UserListView(ListView):
    context_object_name = 'users'
    paginate_by = 20
    template_name = 'account/user_list.html'

    def get_queryset(self):
        if self.request.GET.get('account') != None:
            keyword = self.request.GET.get('account')
            queryset = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword)).order_by('-id')
        else :
            if self.kwargs['group'] == "1":
                queryset = User.objects.filter(groups__name='apply').order_by("-id")
            else :
                queryset = User.objects.all().order_by('-id')
        return queryset
                        
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['group'] = self.kwargs['group']
        context['account'] = self.request.GET.get('account')
        return context								
                            
# 訊息
class MessageListView(ListView):
    context_object_name = 'messages'
    paginate_by = 20
    template_name = 'account/dashboard.html'

    def get_queryset(self):             
        query = []
        #公告
        if self.kwargs['action'] == "1":
            messagepolls = MessagePoll.objects.filter(reader_id=self.request.user.id, message_type=1).order_by('-message_id')
        #私訊
        elif self.kwargs['action'] == "2":
            messagepolls = MessagePoll.objects.filter(reader_id=self.request.user.id, message_type=2).order_by('-message_id')
        #系統
        elif self.kwargs['action'] == "3":
            messagepolls = MessagePoll.objects.filter(reader_id=self.request.user.id, message_type=3).order_by('-message_id')						
        else :
            messagepolls = MessagePoll.objects.filter(reader_id=self.request.user.id).order_by('-message_id')
        for messagepoll in messagepolls:
            query.append([messagepoll, messagepoll.message])
        return query
        
    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        context['action'] = self.kwargs['action']
        return context

def message(request, messagepoll_id):
    messagepoll = MessagePoll.objects.get(id=messagepoll_id)
    messagepoll.read = True
    messagepoll.save()
    message = Message.objects.get(id=messagepoll.message_id)
    return redirect(message.url)			

# 所有註冊學校
def schools(request):
    schools = School.objects.all()
    return render_to_response('account/schools.html',{'schools': schools}, context_instance=RequestContext(request))		
    
class SchoolUpdateView(UpdateView):
    model = School
    fields = ['county', 'zone', 'name']
    template_name = 'form.html'
    #success_url = '/teacher/forum/domain/'
    def get_success_url(self):
        succ_url =  '/account/admin/schools'
        return succ_url
    
    # 修改密碼
def password(request, user_id):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.set_password(request.POST['password'])
            user.save()
               
            return redirect('homepage')
    else:
        form = PasswordForm()
        user = User.objects.get(id=user_id)

    return render_to_response('form.html',{'form': form, 'user':user}, context_instance=RequestContext(request))

# 修改他人的真實姓名
def adminrealname(request, user_id):
    if request.method == 'POST':
        form = RealnameForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.first_name =form.cleaned_data['first_name']
            user.save()
                
            return redirect('/')
    else:
        teacher = False
        enrolls = Enroll.objects.filter(student_id=user_id)
        for enroll in enrolls:
            classroom = Classroom.objects.get(id=enroll.classroom_id)
            if request.user.id == classroom.teacher_id:
                teacher = True
                break
        if teacher:
            user = User.objects.get(id=user_id)
            form = RealnameForm(instance=user)
        else:
            return redirect("/")

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))
    
# 修改自己的真實姓名
def realname(request):
    if request.method == 'POST':
        form = RealnameForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.first_name =form.cleaned_data['first_name']
            user.save()
                
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = RealnameForm(instance=user)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))

# 修改學校名稱
def adminschool(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.last_name =form.cleaned_data['last_name']
            user.save()
                
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = SchoolForm(instance=user)
                
        school_pool = School.objects.filter(online=True)
        county_pool = County.objects.all()
        zone_pool = Zone.objects.all()
        district = []
        index = 0
        for p in county_pool:
            district.append([p, []])
            index2 = 0
            zones = filter(lambda u: u.county == p.id, zone_pool)
            for q in zones:                
                district[index][1].append([q, []])
                schools = filter(lambda u: u.zone == q.id, school_pool)
                for school in schools :
                    district[index][1][index2][1].append(school)
                index2 = index2 + 1
            index = index + 1
        try :
            school = School.objects.get(id=user.last_name)
        except ObjectDoesNotExist:
            school = School.objects.get(id=1)
    return render_to_response('account/school.html',{'form': form, 'district':district, 'school':school }, context_instance=RequestContext(request))
    
# 修改信箱
def adminemail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.email =form.cleaned_data['email']
            user.save()
           
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = EmailForm(instance=user)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))    

# 記錄積分項目
class LogListView(ListView):
    context_object_name = 'logs'
    paginate_by = 20
    template_name = 'account/log_list.html'
    
    def get_queryset(self):          
        if not self.kwargs['kind'] == "0" :
            queryset = PointHistory.objects.filter(user_id=self.kwargs['user_id'],kind=self.kwargs['kind']).order_by('-id')
        else :
            queryset = PointHistory.objects.filter(user_id=self.kwargs['user_id']).order_by('-id')		
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LogListView, self).get_context_data(**kwargs)
        context['user_id'] = self.kwargs['user_id']
        return context		
            
# 顯示個人檔案
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    enrolls = Enroll.objects.filter(student_id=user_id)
    try: 
        profile = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        profile = Profile(user=user)
        profile.save()

    try:
        hour_of_code = Certificate.objects.get(student_id=user_id)
    except ObjectDoesNotExist:
        hour_of_code = None

    # 計算積分    
    credit = profile.work + profile.assistant + profile.creative
      
    # 學校
    try:
        school_name = School.objects.get(id=int(user.last_name)).name
    except ObjectDoesNotExist:
        school_name = ""
    #檢查是否為教師或同班同學
    user_enrolls = Enroll.objects.filter(student_id=request.user.id)
    for enroll in user_enrolls:
        if is_classmate(user_id, enroll.classroom_id) or request.user.id == 1:
          return render_to_response('account/profile.html',{'hour_of_code':hour_of_code, 'school': school_name, 'enrolls':enrolls, 'profile': profile,'user_id':user_id, 'credit':credit}, context_instance=RequestContext(request))	
    if user_id == str(request.user.id):	
        return render_to_response('account/profile.html',{'hour_of_code':hour_of_code, 'school': school_name, 'enrolls':enrolls, 'profile': profile,'user_id':user_id, 'credit':credit}, context_instance=RequestContext(request))	
    return redirect("/")				
    
# 列出所有日期訪客
class VisitorListView(ListView):
    model = Visitor
    context_object_name = 'visitors'
    template_name = 'account/statics_login.html'    
    paginate_by = 20
    
    def get_queryset(self):       
        visitors = Visitor.objects.all().order_by('-id')
        queryset = []
        for visitor in visitors:
            queryset.append([int(str(visitor.date)[0:4]), int(str(visitor.date)[4:6]),int(str(visitor.date)[6:8]),visitor])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(VisitorListView, self).get_context_data(**kwargs)
        first_element = Visitor.objects.all().order_by("-id")[0]
        end_year = int(str(first_element.date)[0:4])
        last_element = Visitor.objects.all().order_by("id")[0]
        start_year = int(str(last_element.date)[0:4])
        context['height'] = 200+ (end_year-start_year)*200
        visitors = Visitor.objects.all().order_by('id')
        queryset = []
        for visitor in visitors:
            queryset.append([int(str(visitor.date)[0:4]), int(str(visitor.date)[4:6]),int(str(visitor.date)[6:8]),visitor])
        context['total_visitors'] = queryset
        return context	
            
# 列出單日日期訪客
class VisitorLogListView(ListView):
    model = VisitorLog
    context_object_name = 'visitorlogs'
    template_name = 'account/statics_login_log.html'    
    paginate_by = 50
    
    def get_queryset(self):
        # 記錄系統事件
        visitor = Visitor.objects.get(id=self.kwargs['visitor_id'])    
        queryset = VisitorLog.objects.filter(visitor_id=self.kwargs['visitor_id']).order_by('-id')
        return queryset
        
    def render_to_response(self, context):
        if not self.request.user.is_authenticated():
            return redirect('/')
        return super(VisitorLogListView, self).render_to_response(context)	

# Ajax 設為教師、取消教師
@user_passes_test(lambda u: u.is_superuser)
def make(request):
    user_id = request.POST.get('userid')
    action = request.POST.get('action')
    if user_id and action :
        user = User.objects.get(id=user_id)           
        try :
            group = Group.objects.get(name="teacher")	
        except ObjectDoesNotExist :
            group = Group(name="teacher")
            group.save()
        if action == 'set':                                  
            group.user_set.add(user)
            # create Message
            title = "<" + request.user.first_name + u">設您為教師"
            url = "/teacher/classroom"
            message = Message(title=title, url=url, time=timezone.now())
            message.save()                        
                    
            # message for group member
            messagepoll = MessagePoll(message_id = message.id,reader_id=user_id)
            messagepoll.save()    
        else :   
            group.user_set.remove(user)  
            # create Message
            title = "<"+ request.user.first_name + u">取消您為教師"
            url = "/"
            message = Message(title=title, url=url, time=timezone.now())
            message.save()                        
                    
            # message for group member
            messagepoll = MessagePoll(message_id = message.id,reader_id=user_id)
            messagepoll.save()               
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'no'}, safe=False)        

def avatar(request):
    profile = Profile.objects.get(user = request.user)      
    return render_to_response('account/avatar.html', {'avatar':profile.avatar}, context_instance=RequestContext(request))
  
# 列出所有私訊
class LineListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'account/line_list.html'    
    paginate_by = 20
    
    def get_queryset(self):     
        queryset = Message.objects.filter(author_id=self.request.user.id).order_by("-id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LineListView, self).get_context_data(**kwargs)
        return context	 
        
# 列出同學以私訊
class LineClassListView(ListView):
    model = Enroll
    context_object_name = 'enrolls'
    template_name = 'account/line_class.html'   
    
    def get_queryset(self):     
        queryset = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("seat")
        return queryset
        
    # 限本班同學
    def render_to_response(self, context):
        if not is_classmate(self.request.user.id, self.kwargs['classroom_id']):
            return redirect('/')
        return super(LineClassListView, self).render_to_response(context)            
                
#新增一個私訊
class LineCreateView(CreateView):
    model = Message
    context_object_name = 'messages'    
    form_class = LineForm
    template_name = 'account/line_form.html'     

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user_name = User.objects.get(id=self.request.user.id).first_name
        self.object.title = u"[私訊]" + user_name + ":" + self.object.title
        self.object.author_id = self.request.user.id
        self.object.reader_id = self.kwargs['user_id']
        self.object.type = 2
        self.object.save()
        self.object.url = "/account/line/detail/" + self.kwargs['classroom_id'] + "/" + str(self.object.id)
        self.object.classroom_id = 0 - int(self.kwargs['classroom_id'])
        self.object.save()
        if self.request.FILES:
            for file in self.request.FILES.getlist('files'):
                content = MessageContent()
                fs = FileSystemStorage()
                filename = uuid4().hex
                content.title = file.name
                content.message_id = self.object.id
                content.filename = str(self.request.user.id)+"/"+filename
                fs.save("static/attach/"+str(self.request.user.id)+"/"+filename, file)
                content.save()
        # 訊息
        messagepoll = MessagePoll(message_id=self.object.id, reader_id=self.kwargs['user_id'], message_type=2, classroom_id=0-int(self.kwargs['classroom_id']))
        messagepoll.save()              
        return redirect("/account/line/")      
        
    def get_context_data(self, **kwargs):
        context = super(LineCreateView, self).get_context_data(**kwargs)
        context['user_id'] = self.kwargs['user_id']
        context['classroom_id'] = self.kwargs['classroom_id']
        messagepolls = MessagePoll.objects.filter(reader_id=self.kwargs['user_id'],  classroom_id=0 - int(self.kwargs['classroom_id'])).order_by('-id')
        messages = []
        for messagepoll in messagepolls:
            message = Message.objects.get(id=messagepoll.message_id)
            if message.author_id == self.request.user.id :
                messages.append([message, messagepoll.read])
        context['messages'] = messages
        return context	 
        
#回覆一個私訊
class LineReplyView(CreateView):
    model = Message
    context_object_name = 'messages'    
    form_class = LineForm
    template_name = 'account/line_form_reply.html'     

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user_name = User.objects.get(id=self.request.user.id).first_name
        self.object.title = u"[私訊]" + user_name + ":" + self.object.title
        self.object.author_id = self.request.user.id
        self.object.reader_id = self.kwargs['user_id']
        self.object.type = 2
        self.object.save()
        self.object.url = "/account/line/detail/" + self.kwargs['classroom_id'] + "/" + str(self.object.id)
        self.object.classroom_id = 0 - int(self.kwargs['classroom_id'])
        self.object.save()
        if self.request.FILES:
            for file in self.request.FILES.getlist('files'):
                content = MessageContent()
                fs = FileSystemStorage()
                filename = uuid4().hex
                content.title = file.name
                content.message_id = self.object.id
                content.filename = str(self.request.user.id)+"/"+filename
                fs.save("static/attach/"+str(self.request.user.id)+"/"+filename, file)
                content.save()
        # 訊息
        messagepoll = MessagePoll(message_id=self.object.id, reader_id=self.kwargs['user_id'], message_type=2, classroom_id=0-int(self.kwargs['classroom_id']))
        messagepoll.save()              
        return redirect("/account/line/")      
        
    def get_context_data(self, **kwargs):
        context = super(LineReplyView, self).get_context_data(**kwargs)
        context['user_id'] = self.kwargs['user_id']
        context['classroom_id'] = self.kwargs['classroom_id']
        message = Message.objects.get(id=self.kwargs['message_id'])
        title = "RE:" + message.title[message.title.find(":")+1:]
        context['title'] = title
        messagepolls = MessagePoll.objects.filter(reader_id=self.kwargs['user_id'],  classroom_id=0 - int(self.kwargs['classroom_id'])).order_by('-id')
        messages = []
        for messagepoll in messagepolls:
            message = Message.objects.get(id=messagepoll.message_id)
            if message.author_id == self.request.user.id :
                messages.append([message, messagepoll.read])
        context['messages'] = messages
        return context	 
			
# 查看私訊內容
def line_detail(request, classroom_id, message_id):
    message = Message.objects.get(id=message_id)
    files = MessageContent.objects.filter(message_id=message_id)
    messes = Message.objects.filter(author_id=message.author_id, reader_id=request.user.id).order_by("-id")
    try:
        if message.type == 2:
            messagepoll = MessagePoll.objects.get(message_id=message_id)
        else:
            messagepoll = MessagePoll.objects.get(message_id=message_id, reader_id=request.user.id)
        if request.user.id == messagepoll.reader_id:
            messagepoll.read = True
        messagepoll.save()
    except :
        messagepoll = MessagePoll()
    return render_to_response('account/line_detail.html', {'files':files, 'lists':messes, 'classroom_id':classroom_id, 'message':message, 'messagepoll':messagepoll}, context_instance=RequestContext(request))

# 下載檔案
def line_download(request, file_id):
    content = MessageContent.objects.get(id=file_id)
    filename = content.title
    download =  settings.BASE_DIR + "/static/attach/" + content.filename
    wrapper = FileWrapper(file( download, "r" ))
    response = HttpResponse(wrapper, content_type = 'application/force-download')
    #response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename.encode('utf8'))
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
	
# 顯示圖片
def line_showpic(request, file_id):
        content = MessageContent.objects.get(id=file_id)
        return render_to_response('student/forum_showpic.html', {'content':content}, context_instance=RequestContext(request))
