# coding=utf-8
import os

from django.shortcuts import render

from .models import *

from django.http import StreamingHttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.db import connection
from django.shortcuts import render_to_response
from django.shortcuts import render

from .utils import *

from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.contrib import messages

# 学生页左半部
def student_left(request):
	return rander_to_response('student_left.html')


# 主页
def index(request):
	return render_to_response('index.html')


# 头部
def header(request):
	if 'id' in request.session and request.session['id'] \
			and 'type' in request.session and request.session['type']:
		tp = request.session['type']
		uid = request.session['id']
		if tp == 's':
			per = Student.objects.get(id=uid)
			str = "Student"
			return render(request, "header.html", {'str': str, 'per': per})
		elif tp == 't':
			per = Teacher.objects.get(id=uid)
			str = "Teacher"
			return render(request, "header.html", {'str': str, 'per': per})
		elif tp == 'e':
			per = EduAdmin.objects.get(id=uid)
			str = "Administrator"
			return render(request, "header.html", {'str': str, 'per': per})
		else:
			return HttpResponseRedirect("/EducationalSystem/")
	else:
		return HttpResponseRedirect("/EducationalSystem/")


# 教师页左部
def teacher_left(request):
	return render_to_response('teacher_left.html')

# 添加课程，单独页面
def jiaowu_addcourse(request):
	tm = Term.objects.filter(is_over=False).order_by("-start")
	return render(request, "jiaowu_addcourse.html", {'tm': tm})


# 添加学期，单独页面
def jiaowu_addsemester(request):
	return render_to_response('jiaowu_addsemester.html')

# 课程信息：教务，单独页面
def jiaowu_courseinfo(request, cou_id):
	course = Course.objects.get(id=cou_id)
	tid = course.term_id
	#term = Term.objects.get(id=tid)
	return render(request, "jiaowu_courseinfo.html", {'course':course, 'term':tid})

# 学生课程，单独页面
def displayCourseForStudent(request):
	if 'id' in request.session and request.session['id'] \
			and 'type' in request.session and request.session['type'] == 's':
		thisTerm = Term.objects.all()
		sid = request.session['id']
		student_course = Course_Student.objects.filter(student_id__id=sid)
		cou_id = student_course.values("course_id")
		cou = Course.objects.filter(term_id__id__in=thisTerm, id__in=cou_id)
		if len(cou) < 3:
			cou1 = cou[0:len(cou)]
			cou2 = None
			return render(request, "student.html", {'cou1': cou1, 'cou2': cou2})
		elif len(cou) < 6:
			cou1 = cou[0:4]
			cou2 = cou[3:len(cou)]
			return render(request, "student.html", {'cou1': cou1, 'cou2': cou2})
		else:
			cou1 = cou[0:4]
			cou2 = cou[3:7]
			return render(request, "student.html", {'cou1': cou1, 'cou2': cou2})
	else:
		return HttpResponseRedirect("/EducationalSystem/")
	# if 'id' in request.GET and request.GET['id']:
	# 	if 'term_id' in request.GET and request.GET['term_id']:
	# 		stu_id = request.GET['id']
	# 		term_id = request.GET['term_id']
	# 		student_course = Course_Student.objects.filter(student_id__id=id)
	# 		course_id = student_course.course_id__id
	# 		ret_course = Course(term_id__id=term_id, id__in=course_id)

#展示课程：教师
def displayCourseForTeacher(request):
	if 'id' in request.session and request.session['id'] \
			and 'type' in request.session and request.session['type'] == 't':
		thisTerm = Term.objects.all()
		tid = request.session['id']
		teacher_course = Course_Teacher.objects.filter(teacher_id__id=tid)
		cou_id = teacher_course.values("course_id")
		cou = Course.objects.filter(term_id__id__in=thisTerm, id__in=cou_id)
		if len(cou) < 3:
			cou1 = cou[0:len(cou)]
			cou2 = None
		elif len(cou) < 6:
			cou1 = cou[0:4]
			cou2 = cou[3:len(cou)]
		else:
			cou1 = cou[0:4]
			cou2 = cou[3:7]
		return render(request, "teacher.html", {'cou1': cou1, 'cou2': cou2})
	else:
		return HttpResponseRedirect("/EducationalSystem/")

#登陆功能，处理函数
def login(request):
	if 'name' in request.POST and request.POST['name'] \
		and 'password' in request.POST and request.POST['password'] \
		and 'type' in request.POST and request.POST['type']:
		userName = request.POST['name']
		userPassword = request.POST['password']
		userKind = request.POST['type']

		if userKind == 't':
			tea = Teacher.objects.get(number = userName, password = userPassword)
			if tea:
				print('successT')
				request.session["id"] = tea.id
				request.session["type"] = "t"
				return HttpResponseRedirect("/EducationalSystem/teacher/")
			return HttpResponseRedirect("/EducationalSystem/")
			# if tea:
			# 	return render_to_response('index.html')
			# else:
			# 	return render_to_response('index.html')
		elif userKind == 's':
			stu = Student.objects.get(number = userName, password = userPassword)
			if stu:
				print('successS')
				request.session["id"] = stu.id
				request.session["type"] = "s"
				return HttpResponseRedirect("/EducationalSystem/student/")
			return HttpResponseRedirect("/EducationalSystem/")
			# 	return render_to_response('index.html')
			# else:
			# 	return render_to_response('index.html')
		elif userKind == "e":
			ea = EduAdmin.objects.get(number = userName, password = userPassword)
			if ea:
				print('successE')
				request.session["id"] = ea.id
				request.session["type"] = "e"
				return HttpResponseRedirect("/EducationalSystem/jiaowu/")
			return HttpResponseRedirect("/EducationalSystem/")
			# if ea:
			# 	return render_to_response('index.html')
			# else:
			# 	return render_to_response('index.html')
		else:
			return HttpResponseRedirect("/EducationalSystem/")
	else:
		return HttpResponseRedirect("/EducationalSystem/")

# 注销功能，处理函数
def logout(request):
	try:
		del request.session['id']
		del request.session['type']
	except KeyError:
		pass
	return HttpResponseRedirect("/EducationalSystem/")


# 展示所有课程：教务 单独页面
def displayCourseForEA(request):
	if 'id' in request.session and request.session['id'] \
			and 'type' in request.session and request.session['type'] == 'e':
		terms = Term.objects.order_by("-id")
		thisTerm = terms[0].id
		cou = Course.objects.filter(term_id__id=thisTerm)
		if len(cou) < 3:
			cou1 = cou[0:len(cou)]
			cou2 = None
		elif len(cou) < 6:
			cou1 = cou[0:4]
			cou2 = cou[3:len(cou)]
		else:
			cou1 = cou[0:4]
			cou2 = cou[3:7]
		return render(request, "jiaowu.html", {'terms': terms, 'cou1': cou1, 'cou2': cou2})
	else:
		return HttpResponseRedirect("/EducationalSystem/")


# 展示个人信息
def displayUserInfo(request):
	if 'id' in request.GET and request.GET['id']:
		if 'kind' in request.GET and request.GET['kind']:
			user_id = request.GET['id']
			userKind = request.GET['kind']

			if userKind == 's':
				stu = Student.objects.get(id=user_id)
			elif userKind == 't':
				tea = Teacher.objects.get(id=user_id)
			elif userKind == 'e':
				ea = EduAdmin.objects.get(id=user_id)


# 保存学期信息，处理函数
def saveTermInfo(request):
	if 'semester_name' in request.GET and 'semester_startdate' in request.GET \
			and 'semester_enddate' in request.GET and 'semester_numofweeks' in request.GET \
			and request.GET['semester_name'] and request.GET['semester_startdate'] \
			and request.GET['semester_enddate'] and request.GET['semester_numofweeks'] \
			and 'selectterm' in request.GET and request.GET['selectterm']:
		name = request.GET['semester_name']
		start = request.GET['semester_startdate']
		end = request.GET['semester_enddate']
		week = request.GET['semester_numofweeks']
		term = request.GET['selectterm']

		term_tmp = Term(name=name, start=start, end=end, week=week, term_id=term)
		term_tmp.save()
		return HttpResponseRedirect("/EducationalSystem/jiaowu/")
	else:
		return HttpResponseRedirect("/EducationalSystem/jiaowu/")

#关闭学期
def closeTerm(request):
	if 'id' in request.GET and request.GET['id']:
		name = request.GET['id']
		term = Term.objects.get(id=id)
		term.is_over = True
		term.save()


# 添加课程，处理函数
def addCourse(request):
	if 'course_name' in request.GET and 'course_point' in request.GET \
			and 'course_time' in request.GET and 'course_location' in request.GET \
			and 'selectterm' in request.GET and 'course_timelength' in request.GET \
			and request.GET['course_point'] and request.GET['course_time'] \
			and request.GET['course_name'] and request.GET['course_timelength'] \
			and request.GET['course_location'] and request.GET['selectterm'] \
			and 'course_teacher' in request.GET and request.GET['course_teacher']:

		name = request.GET['course_name']
		credit = request.GET['course_point']
		time = request.GET['course_time']
		hour = request.GET['course_timelength']
		location = request.GET['course_location']
		term_id = request.GET['selectterm']
		tea_num = request.GET['course_teacher']
		Tea = Teacher.objects.get(number=tea_num)
		if not Tea:
			return HttpResponseRedirect("/EducationalSystem/jiaowu/")
		term = Term.objects.get(id=term_id)
		Course_tmp = Course(name=name, credit=credit, time=time, location=location, term_id=term, hour=hour, tea_id=Tea)
		Course_tmp.save()
		return HttpResponseRedirect("/EducationalSystem/jiaowu/")
	else:
		return HttpResponseRedirect("/EducationalSystem/jiaowu/")

#def setTeacher(request):
#czy
#展示所有资源：教师/学生
def displayAllResource(request):
	if 'course_id' in request.GET and request.GET['course_id'] and \
					'virtual_path' in request.GET and request.GET['virtual_path']:
		course_id = request.GET['course_id']
		virtual_path = request.GET['virtual_path']
		res = Resource.objects.filter(course_id__id=course_id, virtual_path=virtual_path)


# 上传资源：教师
def addResource(request):
	if 'name' in request.GET and request.GET['name'] and \
					'path' in request.GET and request.GET['path'] and \
					'virtual_path' in request.GET and request.GET['virtual_path'] and \
					'course_id' in request.GET and request.GET['course_id']:
		course_id = request.GET['course_id']
		name = request.GET['name']
		path = request.GET['path']
		virtual_path = request.GET['virtual_path']

		Resource_tmp = Resource(name=name, path=path, virtual_path=virtual_path, course_id=course_id)
		Resource_tmp.save()


# mine


# 展示所有作业
def displayCourseAssignments(request):
	if 'id' in request.GET and request.GET['id']:
		cur_id = request.GET['id']
		cur_ass = Assignment.objects.GET(course_id=cur_id)


# 展示作业信息：教师
def displayAssignmentsForTeacher(request):
	if 'id' in request.GET and request.GET['id']:
		ass_id = request.GET['id']
		stu_ass = Assignment_Resource.objects.filter(team_asn_id__asn_id__id=ass_id)
		ass_info = Assignment.objects.GET(id=ass_id)


# 展示作业信息：学生
def displayAssignmentsForStudents(request):
	if 'id' in request.GET and request.GET['id'] \
			and 'id' in request.session and request.session['id']:
		ass_id = request.GET['id']
		stu_id = request.session['id']
		ass_info = Assignment.objects.GET(id=ass_id)
		stu_team = Student_Team.objects.GET(student_id=stu_id, is_approved=True, team_id__course_id=ass_info.course_id)
		ass_res = Assignment_Resource.objects.filter(team_asn_id__team_id=stu_team.id)


def uploadResource(request):
	if request.method == 'POST' and request.session['cid']:
		cur_id = request.session['cid']
		myFiles = request.FILES.getlist("mylists", None)
		if not myFiles:
			dstatus = ("No file to upload")
		for f in myFiles:
			destination = open('E:/upload/', 'wb+')
			res = Resource(name=f.name, path=destination, course_id=cur_id, virtual_path=destination)
			res.save()
			for chunk in f.chunks():
				destination.write(chunk)
			destination.close()
		return HttpResponse("upload over!")


def downloadResource(request):
	if 'fid' in request.GET and request.GET['fid']:
		fid = request.GET['fid']
		myFile = Resource.objects.GET(id = fid)
		fname = myFile.name
		fpath = myFile.path
		def fileIterator(fname, chunk_size = 512):
			with open(fname) as f:
				while(True):
					c = f.read(chunk_size)
					if c:
						yield c
					else:
						break
		response = StreamingHttpResponse(fileIterator(fname))
		response['Content-Type'] = 'application/octet-stream'
		response['Content-Disposition'] = 'attachment;filename = "{0}"'.format(fname)
		return response



#评论学生作业：教师
def setTeamAssignmentComment(request):
	if 'TA_id' in request.GET and request.GET['TA_id'] and \
					'comment' in request.GET and request.GET['comment']:
		TA_id = request.GET['TA_id']
		comment = request.GET['comment']

		TA_tmp = Team_Assignment(id=TA_id)
		TA_tmp.comment = comment
		TA_tmp.save()


# 给作业成绩：教师
def setTeamAssignmentMark(request):
	if 'TA_id' in request.GET and request.GET['TA_id'] and \
					'mark' in request.GET and request.GET['mark']:
		TA_id = request.GET['TA_id']
		mark = request.GET['mark']

		TA_tmp = Team_Assignment(id=TA_id)
		TA_tmp.mark = mark
		TA_tmp.save()

#给作业成绩页面：教师
def displaySetGrade(request):
	return render_to_response("teacher_setgrade.html")

#给评价与成绩：教师
def setTeamAssignmentCommentMark(request,TA_id):
	if 'team_name' in request.GET and request.GET['team_name'] and\
		'homework_name' in request.GET and request.GET['homework_name'] and \
		'homework_grade' in request.GET and request.GET['homework_grade'] and \
		'homework_comment' in request.GET and request.GET['homework_comment']:

		comment = request.GET['homework_comment']
		mark = request.GET['homework_grade']


		TA_tmp = Team_Assignment(id=TA_id)
		TA_tmp.comment = comment
		TA_tmp.mark = mark
		TA_tmp.save()

#展示添加作业页面，单独页面
def displayAddAsn(request, cou_id):
	return render_to_response("teacher_course_homework_add.html")

#添加作业，处理函数
def addAssignment(request, cou_id):

	if 	'assignment_name' in request.GET and request.GET['assignment_name'] and \
		'assignment_requirement' in request.GET and request.GET['assignment_requirement'] and \
		'assignment_starttime' in request.GET and request.GET['assignment_starttime'] and \
		'assignment_duetime' in request.GET and request.GET['assignment_duetime'] and \
		'maximum_submit' in request.GET and request.GET['maximum_submit'] and \
		'grade_ratio' in request.GET and request.GET['grade_ratio']:

		name = request.GET['assignment_name']
		requirement = request.GET['assignment_requirement']
		starttime = request.GET['assignment_starttime']
		duetime = request.GET['assignment_duetime']
		submit_limits = request.GET['maximum_submit']
		weight = request.GET['grade_ratio']
		cou = Course.objects.get(id=cou_id)
		asn = Assignment(name=name, requirement=requirement, starttime=starttime, duetime=duetime, submit_limits =submit_limits, weight=weight, course_id=cou )
		asn.save()

	return HttpResponseRedirect("/EducationalSystem/teacher/")


#展示修改作业页面，单独页面
def displayModAsn(request, asn_id):
	asn = Assignment.objects.get(id=asn_id)
	return render(request, "teacher_course_homework_modify.html", {'asn':asn})

#修改作业，处理函数
def modifyAssignment(request, asn_id):

	if 'assignment_name' in request.GET and request.GET['assignment_name'] and \
		'assignment_requirement' in request.GET and request.GET['assignment_requirement'] and \
		'assignment_starttime' in request.GET and request.GET['assignment_starttime'] and \
		'assignment_duetime' in request.GET and request.GET['assignment_duetime'] and \
		'maximum_submit' in request.GET and request.GET['maximum_submit'] and \
		'grade_ratio' in request.GET and request.GET['grade_ratio']:

		name = request.GET['assignment_name']
		requirement = request.GET['assignment_requirement']
		starttime = request.GET['assignment_starttime']
		duetime = request.GET['assignment_duetime']
		submit_limits = request.GET['maximum_submit']
		weight = request.GET['grade_ratio']

		asn = Assignment.objects.get(id=asn_id)
		asn.name = name
		asn.requirement = requirement
		asn.starttime = starttime
		asn.duetime = duetime
		asn.submit_limits = submit_limits
		asn.weight = weight
		asn.save()
		return HttpResponseRedirect("/EducationalSystem/teacher/")
	else:
		return HttpResponseRedirect("/EducationalSystem/teacher/")


#展示所有作业，单独页面
def displayHwForTea(request, cou_id):
	cou = Course.objects.get(id=cou_id)
	asn = Assignment.objects.filter(course_id=cou)
	return render(request, "teacher_course_homework.html", {'asn': asn, 'cou':cou_id})

def displayCourseInfo(request, course_id):
	course = Course.objects.get(id=course_id)
	term = course.term_id
	return render(request, 'teacher_set_course_basicinfo.html',
				  {'course_id':course.id, 'term_name':term.name,
				   'course_name':course.name, 'time':course.time,
				   'location':course.location, 'credit':course.credit,
				   'hour':course.hour})

#展示单个作业，单独页面
def displayHw(request, asn_id):
	asn = Assignment.objects.get(id=asn_id)
	return render(request, "teacher_course_homework_watchdetails.html", {'asn':asn})

# 删除作业
def deleteAssignment(request, asn_id):
	TA = Team_Assignment.objects.filter(asn_id__id=asn_id)

	Assignment_Resource.objects.filter(team_asn_id__in=TA).delete()
	Student_Grade.objects.filter(team_asn_id__in=TA).delete()

	TA.delete()

	asn = Assignment.objects.get(id=asn_id)
	cou_id = asn.course_id.id
	asn.delete()
	return HttpResponseRedirect("/EducationalSystem/teacher/CouAsn/" + str(cou_id))

#从excel中添加课程学生表条目
def addCourseStudent(request):
	if 'path' in request.GET and request.GET['path']:
		path = request.GET['path']

		num, recs = readFromXLSX(path)

		for i in range(num):
			c_id = recs[i][0].value
			stu_id = recs[i][1].value
			#stu_name = recs[i][2].value

			cour_stu = Course_Student(course_id__id=c_id, stu_id__id=stu_id)
			cour_stu.save()

def setCourseInfo(request, course_id):
	if 'team_uplimit' in request.GET and request.GET['team_uplimit'] and \
					'team_downlimit' in request.GET and request.GET['team_downlimit'] and \
					'other_limit' in request.GET and 'description' in request.GET:
		team_uplimit = request.GET['team_uplimit']
		team_downlimit = request.GET['team_downlimit']
		other_limit = request.GET['other_limit']
		description = request.GET['description']

		course = Course.objects.get(id=course_id)
		course.team_uplimit = team_uplimit
		course.team_downlimit = team_downlimit
		course.other_limit = other_limit
		course.description = description
		course.save()
		return HttpResponseRedirect("/EducationalSystem/teacher/")
		#return HttpResponseRedirect("/EducationalSystem/jiaowu/")

	else:
		return HttpResponseRedirect("/EducationalSystem/teacher/")


def deleteResource(request):
	res = []
	len = 0
	for num in range(10):
		res.append('res_id_'+str(num))
		if res[num] in request.GET and request.GET[res[num]]:
			len = num+1
		else:
			break
	for num in range(len):
		res_id = request.GET[res[num]]
		Resource.objects.get(id=res_id).delete()

def displaySetGrade(request):
	return render_to_response("teacher_setgrade.html")

#展示学生课程信息页面，单独页面
def displayCouForStu(request, cou_id):
	cou = Course.objects.get(id=cou_id)
	term = cou.term_id
	return render(request, "student_course_basicinfo.html", {'cou':cou, 'term':term})

#展示学生所有作业页面，单独页面
def displayHwForStu(request, cou_id):
	cou = Course.objects.get(id=cou_id)
	asn = Assignment.objects.filter(course_id=cou)
	return render(request, "student_course_homework.html", {'cou':cou, 'asn':asn})

#展示学生某一作业，单独页面
def displayStuHw(request, asn_id):
	asn = Assignment.objects.get(id=asn_id)
	cou = asn.course_id
	return render(request, "student_course_homework_watchdetails.html", {'cou':cou, 'asn':asn})
