from django.urls import path
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.logIn,name='login'),
    path('student/<int:id>/<int:id2>/<int:id3>/',views.student,name='register'),
    path('register/',views.register,name='register'),
    path('results/',views.results,name='results'),
    path('logOut/',views.logOut,name='logOut'),
    path('error/',views.error,name='error'),
    path('deptSession/<int:id>/',views.deptSession,name='deptSession'),
    path('deptResult/<int:id>/<int:id2>/',views.deptResult,name='deptResult'),
    path('pdf/<int:id>/',views.pdf_view,name='pdf'),
    path('indAss/<int:id>/',views.indAss,name='indAss'),
    path('pdfs/<int:id>/<int:id2>/<int:id3>/<int:id4>/',views.pdfs_view,name='pdfs'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('teacher/',views.teacher,name='teacher'),
    path('search/',views.search,name='search'),
    path('performance/<int:id>/<int:id2>/',views.performance,name='performance'),
    path('createSession/<int:id>/',views.createSession,name='createSession'),
    path('staff/',views.staff,name='staff'),
    path('semester/<int:id>/<int:id2>/',views.semester,name='semester'),
    path('virtual/<int:id>/<int:id1>/<int:id2>/<int:id3>/<int:id4>/',views.virtual,name='virtual'),
    path('virtualSem/<int:id>/<int:id1>/<int:id2>/<int:id3>/',views.virtualSem,name='virtualSem'),
    path('status/<int:id>/<int:id2>/<int:id3>/',views.status,name='status'),
    path('deptSem/<int:id>/<int:id2>/<int:id3>/',views.deptSem,name="deptSem"),
    path('copo/<int:id>/<int:id2>/<int:id3>/',views.copo,name='copo'),
    path('course/<int:id>/<int:id2>/<int:id3>/',views.course,name='course'),
    path('indCourse/<int:id>/<int:id2>/<int:id3>/<int:id4>/',views.indCourse,name='indCourse'),
    path('cie/<int:id>/<int:id2>/<int:id3>/<int:id4>',views.cie,name='cie'),
    path('cieQuestions/<int:id>/<int:id2>/<int:id3>/<int:id4>',views.cieQuestions,name='cieQuestions'),
    path('semQuestions/<int:id>/<int:id2>/<int:id3>/<int:id4>',views.semQuestions,name='semQuestions'),
    path('labEvaluation/<int:id>/<int:id2>/<int:id3>/<int:id4>',views.labEvaluation,name='labEvaluation'),
    path('finalEvaluation/<int:id>/<int:id2>/<int:id3>/<int:id4>',views.finalEvaluation,name='finalEvaluation'),
    path('generate/<int:id>/<int:id2>/<int:id3>/<int:id4>',views.generate,name='generate'),
    path('assignment/<int:id>/<int:id2>/<int:id3>/<int:id4>',views.assignment,name='assignment'),
    path('nonGenerate/<int:id>/<int:id2>/<int:id3>/<int:id4>',views.nonGenerate,name='nonGenerate'),
    path('attendance/<int:id>/<int:id2>/<int:id3>/<int:id4>',views.attendance,name='attendance'),
    path('courseEvaluation/<int:id>/<int:id2>/<int:id3>/<int:id4>',views.courseEvaluation,name='courseEvaluation'),
    path('tutorial/<int:id>/<int:id2>/<int:id3>/<int:id4>/',views.tutorial,name='tutorial'),
    path('lab/<int:id>/<int:id2>/<int:id3>/<int:id4>/',views.lab,name='lab'),
    path('sem/<int:id>/<int:id2>/<int:id3>/<int:id4>/',views.sem,name='sem'),
    path('nonAtt/<int:id>/<int:id2>/<int:id3>/<int:id4>/',views.nonAtt,name='nonAtt'),
    path('nonEvaluation/<int:id>/<int:id2>/<int:id3>/<int:id4>/',views.nonEvaluation,name='nonEvaluation'),
    path('semResults/<int:id>/<int:id2>/<int:id3>/',views.semResults,name='semResult'),
    path('viewCom/<int:id>/<int:id2>/',views.viewCom,name='viewCom'),
    path('noti/',views.noti,name='noti')

]


