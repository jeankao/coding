# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from survey.models import PreSurvey1, PostSurvey1, PreSurvey2, PostSurvey2, PreSurvey5, PostSurvey5
from student.models import Enroll
from teacher.models import Classroom

pre_questions1 = [
        '1. 我很崇拜程式設計很厲害的人',
        '2. 我對學習程式設計感到有興趣',
        '3. 我認為程式設計可以讓我創作有趣的作品',
        '4. 我希望將來能夠自己設計應用軟體或電腦遊戲',
        '5. 學好程式設計在現代社會中是很重要的',
        '6. 我自信能夠將程式設計所教的基本概念學好',
        '7. 我會盡力將程式設計課程的作業寫好',
        '8. 我覺得程式設計的過程將會非常單調、枯燥',
        '9. 如果老師出的程式設計作業很難，我想我會直接放棄',
        '10. 我和同學或朋友聊天時會談到程式設計相關的事情',
]

post_questions1 = [
        ['一、學習動機', [
            '1. 創作遊戲能夠提高我學習Scratch程式設計的興趣',
            '2. 使用Scratch程式設計撰寫遊戲，讓我覺得很有成就感',
            '3. 學過Scratch創作遊戲後，我覺得學習程式設計概念很無趣',
            '4. 網站積分式的學習，可以促發我的學習動機',
            '5. 網站循序漸進、個別化的學習方式可以促進我學習的動機',
        ]],
        ['二、學習自信', [
            '6. 我覺得Scratch程式設計軟體容易學習',
            '7. 我認為Scratch程式設計可以讓我創作有趣的作品',
            '8. 使用Scratch程式設計撰寫遊戲，讓我覺得很有成就感',
            '9. 學完此門課後，我能精通程式設計的方法與技能',
            '10. 學完此門課後，我能理解程式設計這門課最困難的部分',
        ]],	
        ['三、學習經驗', [
            '11. 我能從Scratch程式設計課程中得到很大的收穫',
            '12. 我能了解影片所講解的觀念並順利完成指派的題目',
            '13. 在實作遊戲時，我很清楚知道自己在做什麼',
            '14. 我會拿自己的學習狀況與同學做比較',
            '15. 學完此課程後，我喜歡程式設計課程的內容',
        ]],
        ['四、學習氣氛', [
            '16. 上課時，多數同學都認真學習並解決問題',
            '17. 上課時，同學會互相觀摩作品與分享彼此想法',
            '18. 上課時，我會詢問老師我不懂的地方，以澄清概念',
            '19. 上課時，當我在這門課遇到不懂的地方時，我會尋求其他同學的幫忙',
            '20. 上課時，教室上課氣氛很愉悅',
        ]],
        ['五、未來發展', [
            '21. 我希望將來能夠自己設計應用軟體或電腦遊戲',
            '22. 學完此課程後，我對學習其他的程式設計感到有興趣',
            '23. 如果學校有開設遊戲設計的社團，我會想要參加',
            '24. 學完此課程後，我認為學好程式設計在現代社會中是很重要的',
            '25. 學完此課程後，我認為我能夠將程式設計課程所學到的（如問題解決、邏輯思考、自學能力與創造力等），運用到其他科目上',
        ]],	
]

post_questions2 = [
        '1. 學習VPhysics之程式設計有助於建立物理的概念 ',
        '2. 學了VPhysics讓我更想學習程式設計技巧',
        '3. 學了VPhysics讓我覺得程式設計很有趣',
        '4. 學完此門課後，我能理解程式設計的基本概念',
        '5. 我覺得學習程式設計，可以讓我做事方法更有信心',
        '6. 我對於在這門課所學到的東西和創作的作品，覺得有成就感',
        '7. 學完此課程後，我認為學好程式設計對我的未來是有幫助的',
        '8. 學完此課程後，我發現程式設計的確可以訓練我的邏輯思考與問題解決能力',
        '9. 只要時間許可，我一定可以把程式學好',
        '10. 學完此課程後，我認為我能夠將程式設計課程所學到的（如問題解決、邏輯思考、與創造力等），運用到其他科目上。',
]
# Create your views here.
def select(request, lesson, classroom_id):
    return render(request, 'survey/select.html', {'classroom_id':classroom_id, 'lesson':lesson})

  # Create your views here.
def pre_result1(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    questionaires = []
    questions = []
    questions.append(['我曾經學過程式設計。',0,0,[]])
    for index, question in enumerate(pre_questions1):
        questions.append([pre_questions1[index],0,0,0,0])
    for enroll in enrolls:
        try:
            questionaire = PreSurvey1.objects.get(student_id=enroll.student_id)
            questions[0][3-questionaire.p]+=1
            questions[0][3].append(questionaire.p_t)
            questions[1][5-questionaire.p1]+=1
            questions[2][5-questionaire.p2]+=1
            questions[3][5-questionaire.p3]+=1
            questions[4][5-questionaire.p4]+=1
            questions[5][5-questionaire.p5]+=1
            questions[6][5-questionaire.p6]+=1
            questions[7][5-questionaire.p7]+=1
            questions[8][5-questionaire.p8]+=1
            questions[9][5-questionaire.p9]+=1
            questions[10][5-questionaire.p10]+=1
            questionaires.append(questionaire)						
        except ObjectDoesNotExist : 
            pass
    return render(request, 'survey/pre_result1.html', {'enrolls':enrolls, 'result':questions, 'questions': pre_questions1, 'classroom':classroom, 'questionaires':questionaires})


def pre_survey1(request):
    try:
        questionaire = PreSurvey1.objects.get(student_id=request.user.id)
    except ObjectDoesNotExist :
        questionaire = PreSurvey1(student_id=request.user.id)
    questions = []
    questions.append([pre_questions1[0], questionaire.p1])		
    questions.append([pre_questions1[1], questionaire.p2])		
    questions.append([pre_questions1[2], questionaire.p3])		
    questions.append([pre_questions1[3], questionaire.p4])
    questions.append([pre_questions1[4], questionaire.p5])		
    questions.append([pre_questions1[5], questionaire.p6])		
    questions.append([pre_questions1[6], questionaire.p7])		
    questions.append([pre_questions1[7], questionaire.p8])		
    questions.append([pre_questions1[8], questionaire.p9])		
    questions.append([pre_questions1[9], questionaire.p10])		
    if request.method == 'POST':
            questionaire.p = request.POST['p1']
            if questionaire.p == "2":
                questionaire.p_t = request.POST['p1t']
            else :
                questionaire.p_t = ""
            questionaire.p1 = request.POST['p2_1']
            questionaire.p2 = request.POST['p2_2']
            questionaire.p3 = request.POST['p2_3']
            questionaire.p4 = request.POST['p2_4']
            questionaire.p5 = request.POST['p2_5']
            questionaire.p6 = request.POST['p2_6']
            questionaire.p7 = request.POST['p2_7']
            questionaire.p8 = request.POST['p2_8']
            questionaire.p9 = request.POST['p2_9']
            questionaire.p10 = request.POST['p2_10']
            questionaire.save()
            return redirect('/student/lesson/A001')
    return render(request, 'survey/pre_survey1.html', {'questionaire':questionaire,'questions': questions})

def pre_teacher1(request, classroom_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    classroom = Classroom.objects.get(id=classroom_id)
    questionaires = []
    for enroll in enrolls:
        questionaire = ""
        try:
            questionaire = PreSurvey1.objects.get(student_id=enroll.student_id)
        except ObjectDoesNotExist :
            questionaire = PreSurvey1(student_id=enroll.student_id)
        questionaires.append([enroll, questionaire])						
    return render(request, 'survey/pre_teacher1.html', {'classroom':classroom,'questionaires':questionaires, 'pre_questions':pre_questions1})

def post_survey1(request):
    try:
        questionaire = PostSurvey1.objects.get(student_id=request.user.id)
    except ObjectDoesNotExist :
        questionaire = PostSurvey1(student_id=request.user.id)
    questions = []
    questions.append([post_questions1[0][0], [[post_questions1[0][1][0], questionaire.p1],[post_questions1[0][1][1], questionaire.p2],[post_questions1[0][1][2], questionaire.p3],[post_questions1[0][1][3], questionaire.p4],[post_questions1[0][1][4], questionaire.p5]]])		
    questions.append([post_questions1[1][0], [[post_questions1[1][1][0], questionaire.p6],[post_questions1[1][1][1], questionaire.p7],[post_questions1[1][1][2], questionaire.p8],[post_questions1[1][1][3], questionaire.p9],[post_questions1[1][1][4], questionaire.p10]]])
    questions.append([post_questions1[2][0], [[post_questions1[2][1][0], questionaire.p11],[post_questions1[2][1][1], questionaire.p12],[post_questions1[2][1][2], questionaire.p13],[post_questions1[2][1][3], questionaire.p14],[post_questions1[2][1][4], questionaire.p15]]])
    questions.append([post_questions1[3][0], [[post_questions1[3][1][0], questionaire.p16],[post_questions1[3][1][1], questionaire.p17],[post_questions1[3][1][2], questionaire.p18],[post_questions1[3][1][3], questionaire.p19],[post_questions1[3][1][4], questionaire.p20]]])
    questions.append([post_questions1[4][0], [[post_questions1[4][1][0], questionaire.p21],[post_questions1[4][1][1], questionaire.p22],[post_questions1[4][1][2], questionaire.p23],[post_questions1[4][1][3], questionaire.p24],[post_questions1[4][1][4], questionaire.p25]]])
    questions_t = []
    questions_t.append(questionaire.p2_1)
    questions_t.append(questionaire.p2_2)
    questions_t.append(questionaire.p2_3)
    if request.method == 'POST':
            questionaire.p1 = request.POST['p2_1_1']
            questionaire.p2 = request.POST['p2_1_2']
            questionaire.p3 = request.POST['p2_1_3']
            questionaire.p4 = request.POST['p2_1_4']
            questionaire.p5 = request.POST['p2_1_5']
            questionaire.p6 = request.POST['p2_2_1']
            questionaire.p7 = request.POST['p2_2_2']
            questionaire.p8 = request.POST['p2_2_3']
            questionaire.p9 = request.POST['p2_2_4']
            questionaire.p10 = request.POST['p2_2_5']
            questionaire.p11 = request.POST['p2_3_1']
            questionaire.p12 = request.POST['p2_3_2']
            questionaire.p13 = request.POST['p2_3_3']
            questionaire.p14 = request.POST['p2_3_4']
            questionaire.p15 = request.POST['p2_3_5']
            questionaire.p16 = request.POST['p2_4_1']
            questionaire.p17 = request.POST['p2_4_2']
            questionaire.p18 = request.POST['p2_4_3']
            questionaire.p19 = request.POST['p2_4_4']
            questionaire.p20 = request.POST['p2_4_5']
            questionaire.p21 = request.POST['p2_5_1']
            questionaire.p22 = request.POST['p2_5_2']
            questionaire.p23 = request.POST['p2_5_3']
            questionaire.p24 = request.POST['p2_5_4']
            questionaire.p25 = request.POST['p2_5_5']
            questionaire.p2_1 = request.POST['t1']
            questionaire.p2_2 = request.POST['t2']
            questionaire.p2_3 = request.POST['t3']
            questionaire.save()

            return redirect('/student/lesson/A011')	
    return render(request, 'survey/post_survey1.html', {'questionaire':questionaire,'questions': questions, 'questions_t':questions_t})

def post_result1(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    questionaires = []
    questions = []
    for index, sections in enumerate(post_questions1):
        questions.append([post_questions1[index][0], [[post_questions1[index][1][0],0,0,0,0],[post_questions1[index][1][1],0,0,0,0],[post_questions1[index][1][2],0,0,0,0],[post_questions1[index][1][3],0,0,0,0],[post_questions1[index][1][4],0,0,0,0]]])
    for enroll in enrolls:
        try:
            questionaire = PostSurvey1.objects.get(student_id=enroll.student_id)
            questions[0][1][0][5-questionaire.p1]+=1
            questions[0][1][1][5-questionaire.p2]+=1
            questions[0][1][2][5-questionaire.p3]+=1
            questions[0][1][3][5-questionaire.p4]+=1
            questions[0][1][4][5-questionaire.p5]+=1
            questions[1][1][0][5-questionaire.p6]+=1
            questions[1][1][1][5-questionaire.p7]+=1
            questions[1][1][2][5-questionaire.p8]+=1
            questions[1][1][3][5-questionaire.p9]+=1
            questions[1][1][4][5-questionaire.p10]+=1
            questions[2][1][0][5-questionaire.p11]+=1
            questions[2][1][1][5-questionaire.p12]+=1
            questions[2][1][2][5-questionaire.p13]+=1
            questions[2][1][3][5-questionaire.p14]+=1
            questions[2][1][4][5-questionaire.p15]+=1
            questions[3][1][0][5-questionaire.p16]+=1
            questions[3][1][1][5-questionaire.p17]+=1
            questions[3][1][2][5-questionaire.p18]+=1
            questions[3][1][3][5-questionaire.p19]+=1
            questions[3][1][4][5-questionaire.p20]+=1
            questions[4][1][0][5-questionaire.p21]+=1
            questions[4][1][1][5-questionaire.p22]+=1
            questions[4][1][2][5-questionaire.p23]+=1
            questions[4][1][3][5-questionaire.p24]+=1
            questions[4][1][4][5-questionaire.p25]+=1
            questionaires.append(questionaire)
        except ObjectDoesNotExist : 
            pass
    return render(request, 'survey/post_result1.html', {'enrolls':enrolls, 'result':questions, 'questions': post_questions1, 'classroom':classroom, 'questionaires':questionaires})

def post_teacher1(request, classroom_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    classroom = Classroom.objects.get(id=classroom_id)
    questionaires = []
    for enroll in enrolls:
        questionaire = ""
        try:
            questionaire = PostSurvey1.objects.get(student_id=enroll.student_id)
        except ObjectDoesNotExist :
            questionaire = PostSurvey1(student_id=enroll.student_id)
        questionaires.append([enroll, questionaire])						
    return render(request, 'survey/post_teacher1.html', {'classroom':classroom,'questionaires':questionaires, 'post_questions':post_questions1})

def pre_survey2(request):
    try:
        questionaire = PreSurvey2.objects.get(student_id=request.user.id)
    except ObjectDoesNotExist :
        questionaire = PreSurvey2(student_id=request.user.id)
    questions = []
    questions.append([pre_questions1[0], questionaire.p1])		
    questions.append([pre_questions1[1], questionaire.p2])		
    questions.append([pre_questions1[2], questionaire.p3])		
    questions.append([pre_questions1[3], questionaire.p4])
    questions.append([pre_questions1[4], questionaire.p5])		
    questions.append([pre_questions1[5], questionaire.p6])		
    questions.append([pre_questions1[6], questionaire.p7])		
    questions.append([pre_questions1[7], questionaire.p8])		
    questions.append([pre_questions1[8], questionaire.p9])		
    questions.append([pre_questions1[9], questionaire.p10])		
    if request.method == 'POST':
            questionaire.p = request.POST['p1']
            if questionaire.p == "2":
                questionaire.p_t = request.POST['p1t']
            else :
                questionaire.p_t = ""
            questionaire.p1 = request.POST['p2_1']
            questionaire.p2 = request.POST['p2_2']
            questionaire.p3 = request.POST['p2_3']
            questionaire.p4 = request.POST['p2_4']
            questionaire.p5 = request.POST['p2_5']
            questionaire.p6 = request.POST['p2_6']
            questionaire.p7 = request.POST['p2_7']
            questionaire.p8 = request.POST['p2_8']
            questionaire.p9 = request.POST['p2_9']
            questionaire.p10 = request.POST['p2_10']
            questionaire.save()
            return redirect('/student/lesson/B01')
    return render(request, 'survey/pre_survey1.html', {'questionaire':questionaire,'questions': questions})

def post_survey2(request):
    try:
        questionaire = PostSurvey2.objects.get(student_id=request.user.id)
    except ObjectDoesNotExist :
        questionaire = PostSurvey2(student_id=request.user.id)
    questions = []
    questions.append([post_questions2[0], questionaire.p1])		
    questions.append([post_questions2[1], questionaire.p2])		
    questions.append([post_questions2[2], questionaire.p3])		
    questions.append([post_questions2[3], questionaire.p4])
    questions.append([post_questions2[4], questionaire.p5])		
    questions.append([post_questions2[5], questionaire.p6])		
    questions.append([post_questions2[6], questionaire.p7])		
    questions.append([post_questions2[7], questionaire.p8])		
    questions.append([post_questions2[8], questionaire.p9])		
    questions.append([post_questions2[9], questionaire.p10])		
    if request.method == 'POST':
            questionaire.p1 = request.POST['p2_1']
            questionaire.p2 = request.POST['p2_2']
            questionaire.p3 = request.POST['p2_3']
            questionaire.p4 = request.POST['p2_4']
            questionaire.p5 = request.POST['p2_5']
            questionaire.p6 = request.POST['p2_6']
            questionaire.p7 = request.POST['p2_7']
            questionaire.p8 = request.POST['p2_8']
            questionaire.p9 = request.POST['p2_9']
            questionaire.p10 = request.POST['p2_10']
            questionaire.p2_1 = request.POST['t1']
            questionaire.p2_2 = request.POST['t2']
            questionaire.p2_3 = request.POST['t3']            
            questionaire.save()
            return redirect('/student/lesson/B16')
    return render('survey/post_survey2.html', {'questionaire':questionaire,'questions': questions})

def pre_result2(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    questionaires = []
    questions = []
    questions.append(['我曾經學過程式設計。',0,0,[]])    
    for index, question in enumerate(pre_questions1):
        questions.append([pre_questions1[index],0,0,0,0])
    for enroll in enrolls:
        try:
            questionaire = PreSurvey2.objects.get(student_id=enroll.student_id)
            questions[0][3-questionaire.p]+=1
            questions[0][3].append(questionaire.p_t)
            questions[1][5-questionaire.p1]+=1
            questions[2][5-questionaire.p2]+=1
            questions[3][5-questionaire.p3]+=1
            questions[4][5-questionaire.p4]+=1
            questions[5][5-questionaire.p5]+=1
            questions[6][5-questionaire.p6]+=1
            questions[7][5-questionaire.p7]+=1
            questions[8][5-questionaire.p8]+=1
            questions[9][5-questionaire.p9]+=1
            questions[10][5-questionaire.p10]+=1
            questionaires.append(questionaire)						
        except ObjectDoesNotExist : 
            pass
    return render(request, 'survey/pre_result1.html', {'enrolls':enrolls, 'result':questions, 'questions': pre_questions1, 'classroom':classroom, 'questionaires':questionaires})

def post_result2(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    questionaires = []
    questions = []
    for index, question in enumerate(post_questions2):
        questions.append([post_questions2[index],0,0,0,0])
    for enroll in enrolls:
        try:
            questionaire = PostSurvey2.objects.get(student_id=enroll.student_id)
            questions[0][5-questionaire.p1]+=1
            questions[1][5-questionaire.p2]+=1
            questions[2][5-questionaire.p3]+=1
            questions[3][5-questionaire.p4]+=1
            questions[4][5-questionaire.p5]+=1
            questions[5][5-questionaire.p6]+=1
            questions[6][5-questionaire.p7]+=1
            questions[7][5-questionaire.p8]+=1
            questions[8][5-questionaire.p9]+=1
            questions[9][5-questionaire.p10]+=1
            questionaires.append(questionaire)						
        except ObjectDoesNotExist : 
            pass
    return render(request, 'survey/post_result2.html', {'enrolls':enrolls, 'result':questions, 'questions': post_questions2, 'classroom':classroom, 'questionaires':questionaires})

def pre_teacher2(request, classroom_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    classroom = Classroom.objects.get(id=classroom_id)
    questionaires = []
    for enroll in enrolls:
        questionaire = ""
        try:
            questionaire = PreSurvey2.objects.get(student_id=enroll.student_id)
        except ObjectDoesNotExist :
            questionaire = PreSurvey2(student_id=enroll.student_id)
        questionaires.append([enroll, questionaire])						
    return render(request,'survey/pre_teacher1.html', {'classroom':classroom,'questionaires':questionaires, 'pre_questions':pre_questions1},context_instance=RequestContext(request))
  
  
def post_teacher2(request, classroom_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    classroom = Classroom.objects.get(id=classroom_id)
    questionaires = []
    for enroll in enrolls:
        questionaire = ""
        try:
            questionaire = PostSurvey2.objects.get(student_id=enroll.student_id)
        except ObjectDoesNotExist :
            questionaire = PostSurvey2(student_id=enroll.student_id)
        questionaires.append([enroll, questionaire])						
    return render(request, 'survey/post_teacher2.html', {'classroom':classroom,'questionaires':questionaires, 'post_questions':post_questions2})

  
def pre_survey5(request):
    try:
        questionaire = PreSurvey5.objects.get(student_id=request.user.id)
    except ObjectDoesNotExist :
        questionaire = PreSurvey5(student_id=request.user.id)
    questions = []
    questions.append([pre_questions1[0], questionaire.p1])		
    questions.append([pre_questions1[1], questionaire.p2])		
    questions.append([pre_questions1[2], questionaire.p3])		
    questions.append([pre_questions1[3], questionaire.p4])
    questions.append([pre_questions1[4], questionaire.p5])		
    questions.append([pre_questions1[5], questionaire.p6])		
    questions.append([pre_questions1[6], questionaire.p7])		
    questions.append([pre_questions1[7], questionaire.p8])		
    questions.append([pre_questions1[8], questionaire.p9])		
    questions.append([pre_questions1[9], questionaire.p10])		
    if request.method == 'POST':
            questionaire.p = request.POST['p1']
            if questionaire.p == "2":
                questionaire.p_t = request.POST['p1t']
            else :
                questionaire.p_t = ""
            questionaire.p1 = request.POST['p2_1']
            questionaire.p2 = request.POST['p2_2']
            questionaire.p3 = request.POST['p2_3']
            questionaire.p4 = request.POST['p2_4']
            questionaire.p5 = request.POST['p2_5']
            questionaire.p6 = request.POST['p2_6']
            questionaire.p7 = request.POST['p2_7']
            questionaire.p8 = request.POST['p2_8']
            questionaire.p9 = request.POST['p2_9']
            questionaire.p10 = request.POST['p2_10']
            questionaire.save()
            return redirect('/student/lesson/E01')
    return render(request, 'survey/pre_survey1.html', {'questionaire':questionaire,'questions': questions})

def post_survey5(request):
    try:
        questionaire = PostSurvey5.objects.get(student_id=request.user.id)
    except ObjectDoesNotExist :
        questionaire = PostSurvey5(student_id=request.user.id)
    questions = []
    questions.append([post_questions2[0], questionaire.p1])		
    questions.append([post_questions2[1], questionaire.p2])		
    questions.append([post_questions2[2], questionaire.p3])		
    questions.append([post_questions2[3], questionaire.p4])
    questions.append([post_questions2[4], questionaire.p5])		
    questions.append([post_questions2[5], questionaire.p6])		
    questions.append([post_questions2[6], questionaire.p7])		
    questions.append([post_questions2[7], questionaire.p8])		
    questions.append([post_questions2[8], questionaire.p9])		
    questions.append([post_questions2[9], questionaire.p10])		
    if request.method == 'POST':
            questionaire.p1 = request.POST['p2_1']
            questionaire.p2 = request.POST['p2_2']
            questionaire.p3 = request.POST['p2_3']
            questionaire.p4 = request.POST['p2_4']
            questionaire.p5 = request.POST['p2_5']
            questionaire.p6 = request.POST['p2_6']
            questionaire.p7 = request.POST['p2_7']
            questionaire.p8 = request.POST['p2_8']
            questionaire.p9 = request.POST['p2_9']
            questionaire.p10 = request.POST['p2_10']
            questionaire.p2_1 = request.POST['t1']
            questionaire.p2_2 = request.POST['t2']
            questionaire.p2_3 = request.POST['t3']            
            questionaire.save()
            return redirect('/student/lesson/E16')
    return render(request, 'survey/post_survey2.html', {'questionaire':questionaire,'questions': questions})

def pre_result5(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    questionaires = []
    questions = []
    questions.append(['我曾經學過程式設計。',0,0,[]])    
    for index, question in enumerate(pre_questions1):
        questions.append([pre_questions1[index],0,0,0,0])
    for enroll in enrolls:
        try:
            questionaire = PreSurvey5.objects.get(student_id=enroll.student_id)
            questions[0][3-questionaire.p]+=1
            questions[0][3].append(questionaire.p_t)
            questions[1][5-questionaire.p1]+=1
            questions[2][5-questionaire.p2]+=1
            questions[3][5-questionaire.p3]+=1
            questions[4][5-questionaire.p4]+=1
            questions[5][5-questionaire.p5]+=1
            questions[6][5-questionaire.p6]+=1
            questions[7][5-questionaire.p7]+=1
            questions[8][5-questionaire.p8]+=1
            questions[9][5-questionaire.p9]+=1
            questions[10][5-questionaire.p10]+=1
            questionaires.append(questionaire)						
        except ObjectDoesNotExist : 
            pass
    return render(request, 'survey/pre_result1.html', {'enrolls':enrolls, 'result':questions, 'questions': pre_questions1, 'classroom':classroom, 'questionaires':questionaires})

def post_result5(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    questionaires = []
    questions = []
    for index, question in enumerate(post_questions2):
        questions.append([post_questions2[index],0,0,0,0])
    for enroll in enrolls:
        try:
            questionaire = PostSurvey5.objects.get(student_id=enroll.student_id)
            questions[0][5-questionaire.p1]+=1
            questions[1][5-questionaire.p2]+=1
            questions[2][5-questionaire.p3]+=1
            questions[3][5-questionaire.p4]+=1
            questions[4][5-questionaire.p5]+=1
            questions[5][5-questionaire.p6]+=1
            questions[6][5-questionaire.p7]+=1
            questions[7][5-questionaire.p8]+=1
            questions[8][5-questionaire.p9]+=1
            questions[9][5-questionaire.p10]+=1
            questionaires.append(questionaire)						
        except ObjectDoesNotExist : 
            pass
    return render(request, 'survey/post_result2.html', {'enrolls':enrolls, 'result':questions, 'questions': post_questions2, 'classroom':classroom, 'questionaires':questionaires})

def pre_teacher5(request, classroom_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    classroom = Classroom.objects.get(id=classroom_id)
    questionaires = []
    for enroll in enrolls:
        questionaire = ""
        try:
            questionaire = PreSurvey5.objects.get(student_id=enroll.student_id)
        except ObjectDoesNotExist :
            questionaire = PreSurvey5(student_id=enroll.student_id)
        questionaires.append([enroll, questionaire])						
    return render(request, 'survey/pre_teacher1.html', {'classroom':classroom,'questionaires':questionaires, 'pre_questions':pre_questions1})
  
  
def post_teacher5(request, classroom_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
    classroom = Classroom.objects.get(id=classroom_id)
    questionaires = []
    for enroll in enrolls:
        questionaire = ""
        try:
            questionaire = PostSurvey5.objects.get(student_id=enroll.student_id)
        except ObjectDoesNotExist :
            questionaire = PostSurvey5(student_id=enroll.student_id)
        questionaires.append([enroll, questionaire])						
    return render(request, 'survey/post_teacher2.html', {'classroom':classroom,'questionaires':questionaires, 'post_questions':post_questions2})
    