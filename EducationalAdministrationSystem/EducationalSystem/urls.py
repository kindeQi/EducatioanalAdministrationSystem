#coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = {
    # 学生页左半部
    url(r'^student_left.html$', views.student_left, name='student_left'),

    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^jiaowu/(\d+)?', views.displayCourseForEA, name='jiaowu'),
    url(r'^jiaowu_change/$', views.changeTerm, name='changeTerm'),
    url(r'^jiaowu_addcourse/$', views.jiaowu_addcourse, name='jiaowu_addcourse'),
    url(r'^jiaowu_addsemester/$', views.jiaowu_addsemester, name='jiaowu_addsemester'),

    # 教务、学生、教师页头部
    url(r'^header.html$', views.header, name = 'header'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^addCourse/$', views.addCourse, name='addCourse'),

    # 教师页左半部
    url(r'^teacher_left.html$', views.teacher_left, name='teacher_left'),
    url(r'^saveTermInfo/$', views.saveTermInfo, name='saveTermInfo'),
    url(r'^student/$', views.displayCourseForStudent, name='student'),
    url(r'^teacher/$', views.displayCourseForTeacher, name='teacher'),
    url(r'^jiaowu_course/(\d+)/$', views.jiaowu_courseinfo, name='jiaowu_courseinfo'),
    url(r'^jiaowu_course/(\d+)/save/$', views.addCourseStudent, name='addCourseStudent'),

    url(r'^teacher/CouAsn/(\d+)/$', views.displayHwForTea, name='displayHwForTea'),
    url(r'^teacher/addAsn/(\d+)/$', views.displayAddAsn, name='displayAddAsn'),
    url(r'^teacher/addAsn/(\d+)/save/$', views.addAssignment, name='addAssignment'),
    url(r'^teacher/modAsn/(\d+)/$', views.displayModAsn, name='displayModAsn'),
    url(r'^teacher/modAsn/(\d+)/save/$', views.modifyAssignment, name='modifyAssignment'),
    url(r'^teacher/Asn/(\d+)/$', views.displayHw, name='displayHw'),
    url(r'^teacher/delAsn/(\d+)/$', views.deleteAssignment, name='deleteAssignment'),

    #url(r'^teacher_set_course_basicinfo/$', views.displaySetCourseInfo, name='teacher_set_course_basicinfo'),
    url(r'^teacher/course/(\d+)/save/$', views.setCourseInfo, name='save_course_info'),
    url(r'^teacher/course/(\d+)/$', views.displayCourseInfo, name='displayCourseInfo'),

    url(r'^student/upldAsn/(\d+)/$', views.uploadHomework, name='uploadAssignment'),
    url(r'^teacher/dldAsn/asn_id(\d+)tid(\d+)/$', views.downloadHomework, name='downloadAssignment'),
    url(r'^teacher/dldAsn/a_id(\d+)/$', views.downloadAllHomework, name='downloadAllHomework'),

    url(r'^teacher/setGd/TA_id(\d+)/$', views.displaySetGrade, name='displaySetGrade'),
    url(r'^teacher/setGd/TA_id(\d+)/save/$', views.setTeamAssignmentCommentMark, name='setTeamAssignmentCommentMark'),

    url(r'^student/course/(\d+)/$', views.displayCouForStu, name='displayCouForStu'),
    url(r'^student/CouAsn/(\d+)/$', views.displayHwForStu, name='displayHwForStu'),
    url(r'^student/Asn/(\d+)/$', views.displayStuHw, name='displayStuHw'),

    url(r'resource/(\d+)/$', views.displayAllResource, name='displayAllResource'),
    url(r'resource/delete/$', views.deleteResource, name='deleteResource'),
    url(r'resource/upload/$', views.uploadResource, name='upload'),
    url(r'resource/doubleclick/$', views.doubleclick, name='doubleclick'),
}
