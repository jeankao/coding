# -*- coding: UTF-8 -*-
from .models import Certificate
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from account.models import Message, MessagePoll, Profile, School
from certificate.forms import ImageUploadForm
from teacher.models import Classroom
from student.models import Enroll
from PIL import Image,ImageDraw,ImageFont
from django.conf import settings
from django.utils.encoding import smart_text
from django.core.files import File 
import cStringIO as StringIO
import os
from django.utils import timezone
from django.http import JsonResponse

# 上傳 Hour of code 證書
def upload_pic(request):
    m = []
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # open file write mode  
            if not os.path.exists(settings.BASE_DIR+"/static/certification/"):
                os.mkdir(settings.BASE_DIR+"/static/certification/")    
            if not os.path.exists(settings.BASE_DIR+"/static/certification/1"):
                os.mkdir(settings.BASE_DIR+"/static/certification/1")
            if not os.path.exists(settings.BASE_DIR+"/static/certification/1/0"):
                os.mkdir(settings.BASE_DIR+"/static/certification/1/0")           
            try:
                m = Certificate.objects.get(student_id=request.user.id)
                m.picture = form.cleaned_data['image']
                
                image_field = form.cleaned_data.get('image')
                image_file = StringIO.StringIO(image_field.read())
                image = Image.open(image_file)
                image = image.resize((900, 640), Image.ANTIALIAS)

                image_file = StringIO.StringIO()
                image.save('static/certification/1/0/'+str(request.user.id)+'.jpg', 'JPEG', quality=90)

                image_field.file = image_file                
                m.save()                              
            except ObjectDoesNotExist:
                m = Certificate(picture=form.cleaned_data['image'], student_id=request.user.id)
                m.save()
            if os.path.isfile(str(m.picture)):
                os.remove(str(m.picture))
            classroom_id = Enroll.objects.filter(student_id=request.user.id).order_by('-id')[0].classroom.id           
            return redirect('/certificate/cert/classroom/1/0/'+str(classroom_id))
    else :
        try:
            m = Certificate.objects.get(student_id=request.user.id)   
        except ObjectDoesNotExist:
            pass
        form = ImageUploadForm()
    return render_to_response('certificate/certificate.html', {'form':form, 'certificate': m}, context_instance=RequestContext(request))


def openFile(fileName, mode, context):
	# open file using python's open method
	# by default file gets opened in read mode
	try:
		fileHandler = open(fileName, mode)
		return {'opened':True, 'handler':fileHandler}
	except IOError:
		context['error'] += 'Unable to open file ' + fileName + '\n'
	except:
		context['error'] += 'Unexpected exception in openFile method.\n'
	return {'opened':False, 'handler':None}

def writeFile(content, fileName, context):
	# open file write mode
	fileHandler = openFile(fileName, 'wb', context)
	
	if fileHandler['opened']:
		# create Django File object using python's file object
		file = File(fileHandler['handler'])
		# write content into the file
		file.write(content)
		# flush content so that file will be modified.
		file.flush()
		# close file
		file.close()

# 顯示證書
def show(request, lesson, unit, enroll_id):
    enroll = Enroll.objects.get(id=enroll_id)
    if lesson == "1" and unit == "0":
        certificate_image = lesson + "/" + unit + "/" + str(request.user.id) + ".jpg"        
    else :
        certificate_image = lesson + "/" + unit + "/" + enroll_id + ".jpg"		
    return render_to_response('certificate/show.html', {'certificate_image': certificate_image}, context_instance=RequestContext(request))
    
    
# 產生證書圖片
def make_image(lesson, unit, enroll_id, teacher_id):
    ''' A View that Returns a PNG Image generated using PIL'''
    im = Image.open(settings.BASE_DIR+'/static/certificate/certificate'+lesson+"_"+unit+'.jpg') # create the image
    draw = ImageDraw.Draw(im)   # create a drawing object that is
                                # used to draw on the new image
    #red = (255,0,0)    # color of our text
    #text_pos = (10,10) # top-left position of our text
    # Now, we'll do the drawing: 
    font_student = ImageFont.truetype(settings.BASE_DIR+'/static/cwTeXQKai-Medium.ttf',60)
    font_school = ImageFont.truetype(settings.BASE_DIR+'/static/cwTeXQKai-Medium.ttf',30)		
    font_teacher = ImageFont.truetype(settings.BASE_DIR+'/static/cwTeXQKai-Medium.ttf',50)    
    font_date = ImageFont.truetype(settings.BASE_DIR+'/static/cwTeXQKai-Medium.ttf',50)  		
    enroll = Enroll.objects.get(id=enroll_id)
    #studnet_id = enroll.student.id
    student_name = User.objects.get(id=enroll.student.id).first_name
    school_name = u"認證教師："+School.objects.get(id=User.objects.get(id=teacher_id).last_name).name  
    lesson_name = "高慧君老師"
    teacher_name = User.objects.get(id=teacher_id).first_name+u"老師"
    year = timezone.localtime(timezone.now()).year
    month = timezone.localtime(timezone.now()).month
    day = timezone.localtime(timezone.now()).day
    date_name = "中 華 民 國 "+ str(year-1911) + " 年 "+ str(month) + " 月 " + str(day) + " 日"
    student = smart_text(student_name, encoding='utf-8', strings_only=False, errors='strict')
    school = smart_text(school_name, encoding='utf-8', strings_only=False, errors='strict')		
    lesson_name = smart_text(lesson_name, encoding='utf-8', strings_only=False, errors='strict')			
    teacher = smart_text(teacher_name, encoding='utf-8', strings_only=False, errors='strict')
    date_string = smart_text(date_name, encoding='utf-8', strings_only=False, errors='strict')		
    draw.text((450,160), student,(0,0,200),font=font_student)		
    draw.text((500,440), teacher,(0,0,0),font=font_teacher)
    draw.text((490,405), school_name,(0,0,0),font=font_school)		
    draw.text((160,520), date_string ,(0,0,0),font=font_date)    
    del draw # I'm done drawing so I don't need this anymore
    
    # We need an HttpResponse object with the correct mimetype
    #response = HttpResponse(content_type = "image/jpeg")
    #im.save(response, 'jpeg')
    #return response
    # now, we tell the image to save as a PNG to the 
    # provided file-like object
    
    temp_handle = StringIO.StringIO()
    im.save(temp_handle, 'jpeg')
    temp_handle.seek(0)
    
    # open file write mode  
    if not os.path.exists(settings.BASE_DIR+"/static/certification/"):
        os.mkdir(settings.BASE_DIR+"/static/certification/")    
    if not os.path.exists(settings.BASE_DIR+"/static/certification/"+lesson):
        os.mkdir(settings.BASE_DIR+"/static/certification/"+lesson)
    if not os.path.exists(settings.BASE_DIR+"/static/certification/"+lesson+"/"+unit):
        os.mkdir(settings.BASE_DIR+"/static/certification/"+lesson+"/"+unit) 
    context = {'error':''}
    fileName = settings.BASE_DIR+"/static/certification/"+lesson+"/"+unit+"/"+enroll_id+".jpg"
    writeFile(temp_handle.read(), fileName, context)

    #update and message
    title = "<" + teacher_name + u">核發了一張證書給你"
    #title = smart_text(teacher_name+"--核發了一張證書給你", encoding='utf-8', strings_only=False, errors='strict')
    url = "/certificate/show/" + lesson + "/" + unit + "/" + enroll_id
    message = Message.create(title=title, url=url, time=timezone.now())
    message.save()
        
    messagepoll = MessagePoll(reader_id=enroll.student.id, message_id = message.id)
    messagepoll.save()
    
def make(request):
    unit = request.POST.get('unit')
    classroom_id = request.POST.get('classroomid')
    enroll_id = request.POST.get('enrollid')
    enroll = Enroll.objects.get(id=enroll_id)	    
    action = request.POST.get('action')
    if classroom_id and enroll_id and action :
        try :
            enroll = Enroll.objects.get(id=enroll_id)	
            if action == 'certificate':
              if leson == "1":
                if unit == "1":
                    enroll.certificate1 = True
                    enroll.certificate1_date = timezone.now()                    
                elif unit == "2":
                    enroll.certificate2 = True
                    enroll.certificate2_date = timezone.now()                    
                elif unit == "3":
                    enroll.certificate3 = True
                    enroll.certificate3_date = timezone.now()                    
                elif unit == "4":
                    enroll.certificate4 = True
                    enroll.certificate4_date = timezone.now()
              elif lesson == "2":
                  enroll.certificate_vphysics = True
                  enroll.certificate_vphysics_date = timezone.now()
              elif lesson == "3":
                  enroll.certificate_euler = True
                  enroll.certificate_euler_date = timezone.now()
              elif lesson == "4":
                  enroll.certificate_vphysics2 = True
                  enroll.certificate_vphysics2_date = timezone.now()                  
              classroom = Classroom.objects.get(id=classroom_id)
              make_image(unit,enroll_id,classroom.teacher_id)              
            else:
              if lesson == "1":
                if unit == "1":
                    enroll.certificate1 = False
                elif unit == "2":
                    enroll.certificate2 = False
                elif unit == "3":
                    enroll.certificate3 = False
                elif unit == "4":
                    enroll.certificate4 = False
              elif lesson == "2":
                enroll.certificate_vphysics = False
              elif lesson == "3":
                enroll.certificate_euler = False
              elif lesson == "4":
                enroll.certificate_vphysics2 = False                
              try :
                  os.remove(settings.BASE_DIR+"/static/certificate/"+unit+"/"+enroll_id+".jpg")	
              except:
                  pass               
            enroll.save()
        except ObjectDoesNotExist :
            pass
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'ko'}, safe=False)
	


# 顯示班級證書    
def classroom(request, lesson, unit, classroom_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    classroom_name = Classroom.objects.get(id=classroom_id).name
    datas = []
    nodatas = []
    for enroll in enrolls:	
        if lesson == "1":
            if unit == "0" :
                try :
                    certificate = Certificate.objects.get(student_id=enroll.student_id)
                    datas.append([enroll, certificate])
                except ObjectDoesNotExist:
                    certificate = []
                    nodatas.append([enroll, []])
		
                def getKey(custom):
                    return custom[1].publish
                datas = sorted(datas, key=getKey)	
            elif unit == "1" :
                    if enroll.certificate1:
	                    datas.append(enroll)
                    else :
                        nodatas.append(enroll)	
            elif unit == "2" :
                    if enroll.certificate2:
       	                datas.append(enroll)
                    else :
                        nodatas.append(enroll)	
            elif unit == "3" :
                    if enroll.certificate3:
	                      datas.append(enroll)
                    else :
                        nodatas.append(enroll)	
            elif unit == "4" :
                    if enroll.certificate4:
	                      datas.append(enroll)
                    else :
		                    nodatas.append(enroll)						
            if unit =="1" :
                def getKey1(custom):
                    return custom.certificate1_date
                datas = sorted(datas, key=getKey1)				
            elif unit == "2":
                def getKey2(custom):
                    return custom.certificate2_date
                datas = sorted(datas, key=getKey2)	
            elif unit == "3":
                def getKey3(custom):
                    return custom.certificate3_date
                datas = sorted(datas, key=getKey3)		
            elif unit == "4":
                def getKey4(custom):
                    return custom.certificate4_date
                datas = sorted(datas, key=getKey4)		

            def getKey5(custom):
                if unit=="0" :
                    return custom[0].seat
                else :
                    return custom.seat
            nodatas = sorted(nodatas, key=getKey5)
        elif lesson == "2":
            if enroll.certificate_vphysics:
	              datas.append(enroll)
            else :
                nodatas.append(enroll)	            
        elif lesson == "3":
            if enroll.certificate_euler:
	              datas.append(enroll)
            else :
                nodatas.append(enroll)	                       
    for student in nodatas:
		    datas.append(student)
    return render_to_response('certificate/classroom.html', {'nodatas':nodatas, 'enrolls':enrolls,'datas': datas, 'unit':unit, 'lesson':lesson}, context_instance=RequestContext(request))
      
def certificate(request, lesson, unit, enroll_id, action):
    if enroll_id and action :
        try :
            enroll = Enroll.objects.get(id=enroll_id)	
            if action == 'certificate':
                if lesson=="1" and unit == "1":
                    enroll.certificate1 = True
                    enroll.certificate1_date = timezone.now()
                elif lesson=="1" and unit == "2":
                    enroll.certificate2 = True
                    enroll.certificate2_date = timezone.now()					
                elif lesson=="1" and unit == "3":
                    enroll.certificate3 = True
                    enroll.certificate3_date = timezone.now()					
                elif lesson=="1" and unit == "4":
                    enroll.certificate4 = True
                    enroll.certificate4_date = timezone.now()	
                elif lesson=="2":
                    enroll.certificate_vphysics = True
                    enroll.certificate_vphysics_date = timezone.now()	     
                elif lesson=="3":
                    enroll.certificate_euler = True
                    enroll.certificate_euler_date = timezone.now()	
                elif lesson=="4":
                    enroll.certificate_vphysics2 = True
                    enroll.certificate_vphysics2_date = timezone.now()                    
                classroom = Classroom.objects.get(id=enroll.classroom_id)
                make_image(lesson, unit,enroll_id,classroom.teacher_id)
             
            else:
                if lesson=="1" and unit == "1":
                    enroll.certificate1 = False
                elif lesson=="1" and unit == "2":
                    enroll.certificate2 = False
                elif lesson=="1" and unit == "3":
                    enroll.certificate3 = False
                elif lesson=="1" and unit == "4":
                    enroll.certificate4 = False	
                elif lesson=="2":
                    enroll.certificate_vphysics = False
                elif lesson=="3":
                    enroll.certificate_euler = False  
                elif lesson=="4":
                    enroll.certificate_vphysics = False                        
            enroll.save()
        except ObjectDoesNotExist :
            enroll = Enroll()
        return redirect('/teacher/memo/'+lesson+"/"+str(enroll.classroom_id))    