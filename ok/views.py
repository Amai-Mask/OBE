from email import message
from functools import reduce
from importlib.resources import open_binary
import re,os
from unittest import findTestCases
import json
import datetime


from decimal import Decimal
import math
from django.db.models import Q
from urllib import response
from io import BytesIO
# from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse,FileResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib import messages
import json
from collections import OrderedDict
import numpy as np
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group,User
from .models import *
from django.contrib.auth.decorators import login_required
@login_required(login_url='/login')
def home(request):
    bo=0
    flag=0
    tea=Teacher.objects.filter(email=request.user.email)
    dept=None
    if not tea:
       bo=1
    else:
       dept=Department.objects.get(deptId=tea[0].dept.deptId)
    cont={
       'bo':bo,
       'flag':flag,
       'user':request.user.username
    }
    return render(request,'home.html',cont)
def search(request):
   bo=0
   tea=Teacher.objects.filter(email=request.user.email)
   dept=None
   if not tea:
      bo=1
   else:
      dept=Department.objects.get(deptId=tea[0].dept.deptId)
   if 'search' in request.POST:
      if request.POST.get('std')=='1':
         ss=None
         if request.POST.get('number'):
            ss=Student.objects.filter(dept=dept,studentId=int(request.POST.get('number')))
         else:
            ss=Student.objects.filter(dept=dept)
         cont={
            'user':request.user.username,
            'cc':ss,
            'bo':bo,
            'flag':1
         }
         return render(request,'search.html',cont)
      elif request.POST.get('std')=='2':
         cc=Student.objects.filter(dept=dept,name__icontains=request.POST.get('text'))
         cont={
            'cc':cc,
            'flag':1,
            'user':request.user.username,
            'bo':bo
         }
         return render(request,'search.html',cont)
      elif request.POST.get('std')=='3':
         cc=Teacher.objects.filter(dept=dept,name__icontains=request.POST.get('text'))
         cont={
            'ss':cc,
            'flag':1,
            'user':request.user.username,
            'bo':bo
         }
         return render(request,'search.html',cont)
   return render(request,'search.html')
def logIn(request):
   if request.method=='POST':
      if request.POST['type']=="1":
        ii=User.objects.filter(email=request.POST['email']).exists()
        bb=Teacher.objects.filter(email=request.POST['email'])
        if ii and bb:
         bb=Teacher.objects.get(email=request.POST['email'])
         pass1=request.POST['pass']
         if bb.password==pass1:
          login(request,authenticate(request,username=bb.username,password=pass1))
          response=redirect('/')
          return response
         else:
          messages.error(request,'Passwords do not match !!',extra_tags='error')
        else:
            messages.error(request, "Please Enter A Valid Email",extra_tags='error')
      elif request.POST['type']=="2":
         ii=User.objects.filter(email=request.POST['email']).exists()
         bb=Student.objects.filter(email=request.POST['email'])
         if ii and bb:
          bb=Student.objects.get(email=request.POST['email'])
          pass1=request.POST['pass']
          if bb.password==pass1:
           login(request,authenticate(request,username=bb.username,password=pass1))
           response=redirect('/')
           return response
          else:
            messages.error(request,'Passwords do not match !!',extra_tags='error')
         else:
            messages.error(request, "Please Enter A Valid Email",extra_tags='error')
      elif request.POST['type']=="3":
         ii=User.objects.filter(email=request.POST['email']).exists()
         bb=Staff.objects.filter(email=request.POST['email'])
         if ii and bb:
          bb=Staff.objects.get(email=request.POST['email'])
          pass1=request.POST['pass']
          if bb.password==pass1:
           login(request,authenticate(request,username=bb.username,password=pass1))
           response=redirect('/')
           return response
          else:
            messages.error(request,'Passwords do not match !!',extra_tags='error')
         else:
            messages.error(request, "Please Enter A Valid Email",extra_tags='error')
   return render(request,'logIn.html')
def logOut(request):
   logout(request)
   return redirect('/login')
def register(request):
    if request.method=='POST':
      if request.POST['type']=="1":
        ii=Teacher.objects.filter(email=request.POST['email'])
        if not not ii:
         bb=Teacher.objects.get(email=request.POST['email'])
         if not not bb.username:
            messages.success(request,"Account Already Exists.",extra_tags='error')
         else:
            pass1=request.POST['pass']
            ii.update(username=request.POST['name'],
            password=pass1
            )
            user=User.objects.create_user(username=request.POST['name'],
            email=bb.email,password=pass1)
            login(request,authenticate(request,username=request.POST['name'],password=pass1))
            messages.success(request, "Account Created Successfully !!!",extra_tags='success')
        else:
            messages.error(request, "Please Enter A Valid Email",extra_tags='error')
      elif request.POST['type']=="2":
         ii=Student.objects.filter(email=request.POST['email'])
         if not not ii:
          bb=Student.objects.get(email=request.POST['email'])
          if not not bb.username:
            messages.success(request,"Account Already Exists.",extra_tags='error')
          else:
            pass1=request.POST['pass']
            ii.update(username=request.POST['name'],
            password=pass1
            )
            user=User.objects.create_user(username=request.POST['name'],email=bb.email,
            password=pass1) 
            login(request,authenticate(request,username=request.POST['name'],password=pass1))
            messages.success(request, "Account Created Successfully !!!",extra_tags='success')
         else:
            messages.error(request, "Please Enter A Valid Email",extra_tags='error')  
      elif request.POST['type']=="3":
         ii=Staff.objects.filter(email=request.POST['email'])
         if not not ii:
          bb=Staff.objects.get(email=request.POST['email'])
          if not not bb.username:
            messages.success(request,"Account Already Exists.",extra_tags='error')
          else:
            pass1=request.POST['pass']
            ii.update(username=request.POST['name'],
            password=pass1
            )
            user=User.objects.create_user(username=request.POST['name'],email=bb.email,
            password=pass1) 
            login(request,authenticate(request,username=request.POST['name'],password=pass1))
            messages.success(request, "Account Created Successfully !!!",extra_tags='success')
         else:
            messages.error(request, "Please Enter A Valid Email",extra_tags='error')  
    return render(request,'register.html')
def createSession(request,id):
   dept=Department.objects.get(deptId=int(id))
   session=Session.objects.filter(dept=dept)
   cont={
      'session':session,
      'dept':dept.deptId
   }
   return render(request,'createSession.html',cont)
   
def semester(request,id,id2):
  dept=Department.objects.get(deptId=int(id2))
  tea=Teacher.objects.get(dept=dept,email=request.user.email)
  chairman=0
  if tea.chairman==1:
     chairman=1
  session=Session.objects.get(dept=dept,session=int(id))
  oo=Semester.objects.filter(dept=dept,session=session).order_by('semester')
  com=Committee.objects.filter(dept=None,session=None)
  cc=Committee.objects.filter(dept=dept,session=session)
  teacher=Teacher.objects.filter(dept=dept)
  year=[]
  for o in com:
     flag=False
     for i in cc:
        if o.comId==i.comId:
           flag=True
     if flag is False:
        year.append(o.comId)
  lost=[1,2,3,4,5,6,7,8]
  last=[]
  for i in lost:
    flag=False
    for o in oo:
     if i==o.semester:
       flag=True
    if not flag:
     last.append(i)
  if 'committee' in request.POST:
     messages.error(request,'oo',extra_tags='com')
  if 'comCreate' in request.POST:
     print(request.POST.get('comId'))
     ok=Committee(
        dept=dept,
        session=session,
        comId=request.POST.get('comId'),
        comChairman=Teacher.objects.get(dept=dept,email=request.POST.get('chairman')),
        comMember1=Teacher.objects.get(dept=dept,email=request.POST.get('mem1')),
        comMember2=Teacher.objects.get(dept=dept,email=request.POST.get('mem2'))
     )
     ok.save()
     cc=''
     if ok.comId=='1':
        cc='1st Year'
     elif ok.comId=='2':
        cc='2nd Year'
     elif ok.comId=='3':
        cc='3rd Year'
     else:
        cc='4th Year'
     sub="You have been assigned as Chairman of "+cc+' exam committee of session '+str(id)+" - "+str(id+1)
     dd=Message.objects.filter()
     ff=Message(
        teacher=Teacher.objects.get(dept=dept,email=ok.comChairman.email),
        text=sub,
        date=datetime.datetime.now(),
        msgId=len(dd)+1
     )
     ff.save()
     sub="You have been assigned as Member of "+cc+' exam committee of session '+str(id)+" - "+str(id+1)
     dd=Message.objects.filter()
     gg=Message(
        teacher=Teacher.objects.get(dept=dept,email=ok.comMember1.email),
        text=sub,
        date=datetime.datetime.now(),
        msgId=len(dd)+1

     )
     gg.save()
     sub="You have been assigned as Member of "+cc+' exam committee of session '+str(id)+" - "+str(id+1)
     dd=Message.objects.filter()
     gg=Message(
        teacher=Teacher.objects.get(dept=dept,email=ok.comMember2.email),
        text=sub,date=datetime.datetime.now(),
        msgId=len(dd)+1
     )
     gg.save()
     url='/semester/'+str(id)+'/'+str(dept.deptId)
     return redirect(url)
  if 'semester' in request.POST:
     messages.error(request,'oo',extra_tags='semester')
  if 'back' in request.POST:
     return redirect('/createSession')
  if 'create' in request.POST:
     oa=Semester(dept=dept,session=session,semester=request.POST.get('semester'))
     oa.save()
     ee=Semester.objects.filter(dept=dept,session=session).order_by('semester')
     cont={
        'last':last,
        'session':session,
        'semester':ee,
        'chairman':chairman,
        'dept':dept.deptId
     }
     return render(request,'semester.html',cont)
  cont={
     'last':last,
     'session':session,
     'semester':oo,
     'year':year,
     'teacher':teacher,
     'chairman':chairman,
     'dept':dept.deptId
   }
  return render(request,'semester.html',cont)
def course(request,id,id2,id3):
   dept=Department.objects.get(deptId=int(id3))
   comChairman=0
   tea=Teacher.objects.get(email=request.user.email)
   cc=int(id2)
   if cc%2==1:
      cc+=1
   session=Session.objects.get(dept=dept,session=int(id))
   com=Committee.objects.get(dept=dept,session=session,comId=(cc/2))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   ooCourse=Course.objects.filter(dept=dept,session=session)
   course=Course.objects.filter(dept=dept,session=session,semester=semester)
   notCourse=Course.objects.filter(dept=dept,session=None)
   teacher=Teacher.objects.filter(dept=dept)
   exts=Teacher.objects.filter()
   quer={}
   for o in exts:
      quer.__setitem__(o.dept.name,[])
   for o in exts:
      quer[o.dept.name].append(o)

   students=Student.objects.filter(dept=dept,session=session)
   last=[]
   kir=0
   if com.comChairman==tea or com.comMember1==tea or com.comMember2==tea:
      kir=1
   if com.comChairman==tea:
      comChairman=1
   if semester.done==1:
      comChairman=0
   for o in notCourse:
      flag=False
      for i in ooCourse:
         if o.courseCode==i.courseCode:
            flag=True
      if flag is False:
         last.append(o)
   if 'back' in request.POST:
      return redirect(str('/semester/')+str(id)+str('/')+str(dept.deptId))
   if 'ok' in request.POST:
      messages.error(request,'ok',extra_tags='course')
   if 'create' in request.POST:
      cor=Course.objects.get(session=None,courseCode=request.POST.get('courseCode'))
      oo=Course(
         dept=dept,
         name=cor.name,
         session=session,
         semester=semester,
         main=Teacher.objects.get(email=request.POST.get('main')),
         external=Teacher.objects.get(email=request.POST.get('external')),
         thirdExaminer=Teacher.objects.get(email=request.POST.get('third')),
         credit=cor.credit,
         courseCode=cor.courseCode,
         obe=cor.obe
      )
      oo.save()
      ss=''
      if id2==1:
         ss='1st Semester'
      elif id2==2:
         ss='2nd Semester'
      elif id2==3:
         ss='3rd Semester'
      else:
         ss=str(id2)+'th Semester'
      dd=Message.objects.filter()
      sub='You have been assigned as Course Teacher of course '+str(oo.name)+' of '+ss+' of session '+str(id)+" - "+str(id+1)
      ff=Message(
         teacher=Teacher.objects.get(email=oo.main.email),
         text=sub,        date=datetime.datetime.now(),
         msgId=len(dd)+1

      )
      ff.save()
      sub='You have been assigned as External of course '+str(oo.name)+' of '+ss+' of session '+str(id)+" - "+str(id+1)
      dd=Message.objects.filter()
      ff=Message(
         teacher=Teacher.objects.get(email=oo.external.email),
         text=sub,date=datetime.datetime.now(),
         msgId=len(dd)+1
      )
      ff.save()
      sub='You have been assigned as Third Examiner of course '+str(oo.name)+' of '+ss+' of session '+str(id)+" - "+str(id+1)
      dd=Message.objects.filter()
      ff=Message(
         teacher=Teacher.objects.get(email=oo.thirdExaminer.email),
         text=sub,date=datetime.datetime.now(),
         msgId=len(dd)+1
      )
      ff.save()
      for o in students:
         oo.student.add(o)
      url='/course/'+str(id)+'/'+str(id2)+'/'+str(id3)
      return redirect(url)
   cont={
      'session':session,
      'semester':semester,
      'course':course,
      'last':last,
      'teacher':teacher,
      'comChairman':comChairman,
      'flag':kir,
      'external':quer,
      'dept':dept.deptId,
   }
   return render(request,'course.html',cont)
def status(request,id,id2,id3):
   dept=Department.objects.get(deptId=int(id3))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   courses=Course.objects.filter(dept=dept,session=session,semester=semester)
   ss=""
   theory=[]
   lab=[]
   if 'pub' in request.POST:
      semester.done=1
      semester.save()
      url="/status/"+str(id)+"/"+str(id2)+"/"+str(id3)+"/"
      return redirect(url)
   for o in courses:
      if o.credit==3:
         theory.append(o)
      else:
         lab.append(o)
   if int(id2)==1:
      ss="1st Semester"
   elif int(id2)==2:
      ss="2nd Semester"
   elif int(id2)==3:
      ss='3rd Semester'
   else:
      ss=str(id2)+"th Semester"
   ss+=' of Session '+str(id)+" - "+str(int(id)+1) 
   cont={
      'ss':ss,
      'theory':theory,
      'lab':lab,
      'dept':id3,
      'session':id,
      'semester':semester
   }
   return render(request,'status.html',cont)
def indCourse(request,id,id2,id3,id4):  
   cc=0 
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   oo=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   bb=int(int(id2+1)/2)
   com=Committee.objects.get(dept=dept,session=session,comId=bb)
   comma=0
   if request.user.email==com.comChairman.email or request.user.email==com.comMember1.email or request.user.email==com.comMember2.email:
      comma=1
   if oo.main.email==request.user.email or oo.thirdExaminer.email==request.user.email or oo.external.email==request.user.email or comma==1:
      cc=1
   if cc==0:
      return redirect('/error')
   if 'back' in request.POST:
      return redirect('/course/'+str(id)+'/'+str(id2)+'/'+str(id3))
   cont={
      'session':id,
      'semester':id2,
      'course':id3,
      'oo':oo,
      'dept':dept.deptId
   }
   return render(request,'indCourse.html',cont)
def error(request):
   return render(request,'error.html')
def cie(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   tea=Teacher.objects.filter(email=request.user.email)
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   uri="/cie/"+str(id)+"/"+str(id2)+"/"+str(id3)+"/"+str(id4)
   if not tea or tea[0]!=course.main:
      return redirect('/error')
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   if course.done==1:
      return redirect('/error')
   cn=0
   cie=CIE.objects.filter(dept=dept,session=session,semester=semester,course=course)
   for o in cie:
      cn=max(cn,o.no)
   cn+=1
   quer={}
   kk=[]
   c=1
   while c<cn:
      ll=CIE.objects.filter(dept=dept,session=session,semester=semester,course=course,no=c).order_by('student__studentId')
      if ll:
         quer.__setitem__(c,ll)
         kk.append(c)
      c+=1
   if 'ans1' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans1'))
      ii=cieQ.objects.get(dept=dept,session=session,semester=semester,course=course,no=cn,student=std)
      filepath = os.path.join('media', str(ii.clo1))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   if 'ans2' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans2'))
      ii=cieQ.objects.get(dept=dept,session=session,semester=semester,course=course,no=cn,student=std)
      filepath = os.path.join('media', str(ii.clo2))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   if 'ans3' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans3'))
      ii=cieQ.objects.get(dept=dept,session=session,semester=semester,course=course,no=cn,student=std)
      filepath = os.path.join('media', str(ii.clo3))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   if 'ans4' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans4'))
      ii=cieQ.objects.get(dept=dept,session=session,semester=semester,course=course,no=cn,student=std)
      filepath = os.path.join('media', str(ii.clo4))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   if 'ans5' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans5'))
      ii=cieQ.objects.get(dept=dept,session=session,semester=semester,course=course,no=cn,student=std)
      filepath = os.path.join('media', str(ii.clo5))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   if 'ans6' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans6'))
      ii=cieQ.objects.get(dept=dept,session=session,semester=semester,course=course,no=cn,student=std)
      filepath = os.path.join('media', str(ii.clo6))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   if 'save' in request.POST:
      oo=CIE.objects.filter(dept=dept,session=session,semester=semester,course=course,no=cn)
      if not oo:
         for o in students:
            pp=CIE(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o.studentId) ,no=cn)
            pp.save()
      for o,i in zip(request.POST.getlist('clo1'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=cn
                            )
         ii.CLO1=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo2'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=cn
                            )
         ii.CLO2=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo3'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=cn
                            )
         ii.CLO3=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo4'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=cn
                            )
         ii.CLO4=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo5'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=cn
                            )
         ii.CLO5=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo6'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=cn
                            )
         ii.CLO6=Decimal(o)
         ii.save()
      for o in students:
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o.studentId),
                            no=cn)     
         ii.total=ii.CLO1+ii.CLO2+ii.CLO3+ii.CLO4+ii.CLO5+ii.CLO6
         ii.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return HttpResponseRedirect(url)
   if 'again' in request.POST:
      kk=int(request.POST['again'])
      for o,i in zip(request.POST.getlist('clo1'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=kk
                            )
         ii.CLO1=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo2'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=kk
                            )
         ii.CLO2=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo3'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=kk
                            )
         ii.CLO3=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo4'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=kk
                            )
         ii.CLO4=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo5'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=kk
                            )
         ii.CLO5=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo6'),students):
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=kk
                            )
         ii.CLO6=Decimal(o)
         ii.save()
      for o in students:
         ii=CIE.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o.studentId),
                            no=kk)     
         ii.total=ii.CLO1+ii.CLO2+ii.CLO3+ii.CLO4+ii.CLO5+ii.CLO6
         ii.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   if 'cancel' in request.POST:
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   ceq=cieQA.objects.filter(dept=dept,session=session,semester=semester,course=course,no=cn)
   if ceq:
      if ceq[0].on==2:
         for o in students:
            ca=cieQ.objects.filter(dept=dept,session=session,semester=semester,course=course,no=cn,student=Student.objects.get(email=o.email))
            if not ca:
               dd=cieQ(
                  dept=dept,session=session,semester=semester,course=course,no=cn,student=Student.objects.get(email=o.email)
               )
               dd.save()
   ara=cieQ.objects.filter(dept=dept,session=session,semester=semester,course=course,no=cn).order_by('student__studentId')
   for o in students:
      print(o.studentId)
   print('majhe')
   for o in ara:
      print(o.student.studentId)
   cont={
      'marks':zip(students,ara),
      'cn':cn,
      'zz':quer,
      'course':course,
      'uri':uri
   }
   return render(request,'cie.html',cont)
def finalEvaluation(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   if course.credit != 3:
      return redirect('/labEvaluation/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4))
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   ok=0
   if course.main.email==request.user.email:
      ok=0
   elif course.external.email==request.user.email:
      ok=1
   elif course.thirdExaminer.email==request.user.email:
      ok=2
   if ok==0 and course.done==1:
      return redirect('/error')
   elif ok==1 and course.extDone==1:
      return redirect('/error')
   elif ok==2 and course.diff==0:
      return redirect('/error')
   elif ok==2 and course.diff==1 and course.thirdDone:
      return redirect('/error')
   
   cie=Final.objects.filter(dept=dept,session=session,semester=semester,course=course,teacher=ok).order_by('student__studentId')
   if not cie:
      for o in students:
         jj=Final(dept=dept,
            session=session,semester=semester,course=course,student=Student.objects.get(email=o.email),
            teacher=ok
         )
         jj.save()
   if 'ans1' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans1'))
      ii=semQ.objects.get(dept=dept,session=session,semester=semester,course=course,student=std)
      filepath = os.path.join('media', str(ii.clo1))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   if 'ans2' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans2'))
      ii=semQ.objects.get(dept=dept,session=session,semester=semester,course=course,student=std)
      filepath = os.path.join('media', str(ii.clo2))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   if 'ans3' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans3'))
      ii=semQ.objects.get(dept=dept,session=session,semester=semester,course=course,student=std)
      filepath = os.path.join('media', str(ii.clo3))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   if 'ans4' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans4'))
      ii=semQ.objects.get(dept=dept,session=session,semester=semester,course=course,student=std)
      filepath = os.path.join('media', str(ii.clo4))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   if 'ans5' in request.POST:
      std=Student.objects.get(studentId=request.POST.get('ans5'))
      ii=semQ.objects.get(dept=dept,session=session,semester=semester,course=course,student=std)
      filepath = os.path.join('media', str(ii.clo5))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   marks=Final.objects.filter(dept=dept,session=session,semester=semester,course=course,teacher=ok).order_by('student__studentId')
   if 'save' in request.POST:
      for o,i in zip(request.POST.getlist('clo1'),students):
         ii=Final.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            teacher=ok
                            )
         ii.semCLO1=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo2'),students):
         ii=Final.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            teacher=ok
                            )
         ii.semCLO2=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo3'),students):
         ii=Final.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            teacher=ok
                            )
         ii.semCLO3=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo4'),students):
         ii=Final.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            teacher=ok
                            )
         ii.semCLO4=Decimal(o)
         ii.save()
      for o,i in zip(request.POST.getlist('clo5'),students):
         ii=Final.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            teacher=ok
                            )
         ii.semCLO5=Decimal(o)
         ii.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   if 'cancel' in request.POST:
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3) +'/'+str(id4)     
      return redirect(url)
   if 'sub' in request.POST:
      if request.user.email==course.main.email:
         course.done=1
         course.save()
      elif request.user.email==course.external.email:
         course.extDone=1
         course.save()
      elif request.user.email==course.thirdExaminer.email:
         course.thirdDone=1
         course.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   sem=semQA.objects.filter(dept=dept,session=session,semester=semester,course=course)
   if sem:
      if sem[0].on==2:
         for o in marks:
            std=Student.objects.get(email=o.student.email)
            da=semQ.objects.filter(dept=dept,session=session,semester=semester,course=course,student=std)
            if not da:
               ee=semQ(
                  dept=dept,session=session,semester=semester,course=course,student=std
               )
               ee.save()
   ara=semQ.objects.filter(dept=dept,session=session,semester=semester,course=course).order_by('student__studentId')
   for o in marks:
      print(o.student.studentId)
   for o in ara:
      print(o.student.studentId)
   cont={
      'marks':zip(marks,ara)
   }
   return render(request,'finalEvaluation.html',cont)
def attendance(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   cc=indAttendance.objects.filter(dept=dept,session=session,semester=semester,course=course)
   today=datetime.datetime.now().date()
   if request.user.email!=course.main.email:
      return redirect('/error')
   elif course.tutDone==1:
      return redirect('/error')
   if not cc:
      aa=indAttendance(dept=dept,session=session,semester=semester,course=course)
      aa.save()
   nn=indAttendance.objects.filter(dept=dept,session=session,semester=semester,course=course,date=today)
   if not nn:
      if 'attendance' in request.POST:
         oo=indAttendance.objects.get(dept=dept,session=session,semester=semester,course=course,student=None)
         oo.present+=1
         oo.save()
         for o in request.POST.getlist('att'):
            ind=indAttendance(
               dept=dept,session=session,semester=semester,course=course,
               student=Student.objects.get(dept=dept,session=session,studentId=int(o)),
               present=1,date=today
            )
            ind.save()
         url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
         return redirect(url)
   else:
         messages.error(request,'Attendance is already taken for today!',extra_tags='taken')
   if 'cancel' in  request.POST:
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   cont={
      'course':course,
      'students':students,
      'date':today
   }
   return render(request,'attendance.html',cont)
def courseEvaluation(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   students=Student.objects.filter(dept=dept,session=session)
   bb=int((int(id2)+1)/2)
   com=Committee.objects.get(dept=dept,session=session,comId=bb)
   comma=0
   if request.user.email==com.comChairman.email or request.user.email==com.comMember1.email or request.user.email==com.comMember2.email:
      comma=1
   if comma==0:
      return redirect('/error')
   kk=False
   if course.done==1 and course.extDone==1:
      if course.diff==1 and course.thirdDone==1:
         kk=True
      elif course.diff==0 :
         kk=True
   if course.done==1 and course.extDone==1:
      jj=CombinedResult.objects.filter(dept=dept,session=session,semester=semester,course=course)
      if not jj:
         bo=False
         if bo is False:      
          for o in students:
            ia=bestOf.objects.get(dept=dept,session=session,semester=semester,course=course,
                               student=Student.objects.get(studentId=o.studentId),
                               )
            ib=Final.objects.get(dept=dept,session=session,semester=semester,course=course,
                               student=Student.objects.get(studentId=o.studentId),
                               teacher=0
                               )
            ic=Final.objects.get(dept=dept,session=session,semester=semester,course=course,
                               student=Student.objects.get(studentId=o.studentId),
                               teacher=1
                               )
            kk=0
            ll=0
            if course.credit==3:
               kk=ib.semCLO1+ib.semCLO2+ib.semCLO3+ib.semCLO4+ib.semCLO5
               ll=ic.semCLO1+ic.semCLO2+ic.semCLO3+ic.semCLO4+ic.semCLO5
            else:
               kk=ib.total
               ll=ic.total
            dif=abs(kk-ll)
            if dif>=12:
               course.diff=1
               course.save()
            oo=CombinedResult(dept=dept,
               session=session,semester=semester,course=course,                        
               student=Student.objects.get(studentId=o.studentId),
               diff=dif,
               finCLO1=ia.CLO1+(ib.semCLO1+ic.semCLO1)/2,
               finCLO2=ia.CLO2+(ib.semCLO2+ic.semCLO2)/2,
               finCLO3=ia.CLO3+(ib.semCLO3+ic.semCLO3)/2,
               finCLO4=ia.CLO4+(ib.semCLO4+ic.semCLO4)/2,
               finCLO5=ia.CLO5+(ib.semCLO5+ic.semCLO5)/2,
               finCLO6=ia.CLO6,
            )
            oo.save()
            oo.total=math.ceil(oo.finCLO1+oo.finCLO2+oo.finCLO3+oo.finCLO4+oo.finCLO5+oo.finCLO6+ia.attendance+ia.lab+ia.assignment+(ib.total+ic.total)/2)
            oo.save()
            cc=oo.total
            dd=0
            if cc >= 80.0:
                dd = 4.00
            elif cc < 80.0 and cc >= 75.0:
                dd = 3.75
            elif cc < 75.0 and cc >= 70:
                dd = 3.50
            elif cc < 70 and cc >= 65.0:
                dd = 3.25
            elif cc < 65.0 and cc >= 60.0:
                dd = 3.00
            elif cc < 60.0 and cc >= 55.0:
                dd = 2.75
            elif cc < 55.0 and cc >= 50.0:
                dd = 2.50
            elif cc < 50.0 and cc >= 45.0:
                dd = 2.25
            elif cc < 45.0 and cc >= 40.00:
                dd = 2.00
            else:
             dd = 0.00
            oo.grade=dd
            oo.save()
      elif course.diff==1 and course.thirdDone==1:
         for o in students:
            ia=bestOf.objects.get(dept=dept,session=session,semester=semester,course=course,
                               student=Student.objects.get(studentId=o.studentId),
                               )
            ib=Final.objects.get(dept=dept,session=session,semester=semester,course=course,
                               student=Student.objects.get(studentId=o.studentId),
                               teacher=2
                               )
            oo=CombinedResult.objects.get(dept=dept,
               session=session,semester=semester,course=course,                        
               student=Student.objects.get(studentId=o.studentId))
            oo.thirdFinCLO1=math.ceil((ia.CLO1)+ib.semCLO1)
            oo.thirdFinCLO2=math.ceil((ia.CLO2)+ib.semCLO2)
            oo.thirdFinCLO3=math.ceil((ia.CLO3)+ib.semCLO3)
            oo.thirdFinCLO4=math.ceil((ia.CLO4)+ib.semCLO4)
            oo.thirdFinCLO5=math.ceil((ia.CLO5)+ib.semCLO5)
            oo.thirdFinCLO6=math.ceil((ia.CLO6))
            oo.save()
            oo.thirdTotal=(oo.thirdFinCLO1+oo.thirdFinCLO2+oo.thirdFinCLO3+oo.thirdFinCLO4+oo.thirdFinCLO5+oo.thirdFinCLO6+ia.attendance+ia.lab+ia.assignment+ib.total)
            oo.save()
            cc=oo.thirdTotal
            dd=0
            if cc >= 80.0:
                dd = 4.00
            elif cc < 80.0 and cc >= 75.0:
                dd = 3.75
            elif cc < 75.0 and cc >= 70:
                dd = 3.50
            elif cc < 70 and cc >= 65.0:
                dd = 3.25
            elif cc < 65.0 and cc >= 60.0:
                dd = 3.00
            elif cc < 60.0 and cc >= 55.0:
                dd = 2.75
            elif cc < 55.0 and cc >= 50.0:
                dd = 2.50
            elif cc < 50.0 and cc >= 45.0:
                dd = 2.25
            elif cc < 45.0 and cc >= 40.00:
                dd = 2.00
            else:
             dd = 0.00
            oo.grade=dd
            oo.save()
      if course.done==1 and course.extDone==1:
         if course.diff==1 and course.thirdDone==1:
            course.finDone=1
            course.save()
         elif course.diff==0:
            course.finDone=1
            course.save()
      kk=CombinedResult.objects.filter(dept=dept,session=session,semester=semester,course=course).order_by('student__studentId')
      cont={
         'marks':kk,
      }
      return render(request,'courseEvaluation.html',cont)

   else:
      messages.error(request,'Course result is not ready yet!',extra_tags='ready')
   return render(request,'courseEvaluation.html')
def tutorial(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   tea=Teacher.objects.filter(email=request.user.email)
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   if not tea or tea[0]!=course.main:
      return redirect('/error')
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   if course.tutDone==1:
      return redirect('/error')
   cn=0
   cie=Tutorial.objects.filter(dept=dept,session=session,semester=semester,course=course)
   for o in cie:
      cn=max(cn,o.no)
   cn+=1
   quer={}
   kk=[]
   c=1
   while c<cn:
      ll=Tutorial.objects.filter(dept=dept,session=session,semester=semester,course=course,no=c).order_by('student__studentId')
      if ll:
         quer.__setitem__(c,ll)
         kk.append(c)
      c+=1
   if 'save' in request.POST:
      oo=Tutorial.objects.filter(dept=dept,session=session,semester=semester,course=course,no=cn)
      if not oo:
         for o in students:
            pp=Tutorial(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o.studentId) ,no=cn)
            pp.save()
      for o,i in zip(request.POST.getlist('tut'),students):
         ii=Tutorial.objects.get(dept=dept,session=session,semester=semester,
                            course=course,student=Student.objects.get(studentId=i.studentId),
                            no=cn
                            )
         ii.tutorial=Decimal(o)
         ii.save()
      for o in students:
         ii=Tutorial.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o.studentId),
                            no=cn)     
         ii.total=ii.tutorial
         ii.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return HttpResponseRedirect(url)
   if 'cancel' in request.POST:
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   cont={
      'marks':students,
      'cn':cn,
      'zz':quer,
      'course':course
   }
   return render(request,'tutorial.html',cont)
def nonAtt(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   cc=indAttendance.objects.filter(dept=dept,session=session,semester=semester,course=course)
   today=datetime.datetime.now().date()
   if request.user.email!=course.main.email:
      return redirect('/error')
   elif course.tutDone==1:
      return redirect('/error')
   if not cc:
      aa=indAttendance(dept=dept,session=session,semester=semester,course=course)
      aa.save()
   nn=indAttendance.objects.filter(dept=dept,session=session,semester=semester,course=course,date=today)
   if not nn:
      if 'attendance' in request.POST:
         oo=indAttendance.objects.get(dept=dept,session=session,semester=semester,course=course,student=None)
         oo.present+=1
         oo.save()
         for o in request.POST.getlist('att'):
            ind=indAttendance(
               dept=dept,session=session,semester=semester,course=course,
               student=Student.objects.get(dept=dept,session=session,studentId=int(o)),
               present=1,date=today
            )
            ind.save()
         url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
         return redirect(url)
   else:
         messages.error(request,'Attendance is already taken for today!',extra_tags='taken')
   if 'cancel' in  request.POST:
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   cont={
      'course':course,
      'students':students,
      'date':today
   }
   return render(request,'attendance.html',cont)
def sem(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   students=Student.objects.filter(dept=dept,session=session)
   ok=3
   print(course.credit)
   if course.credit !=3:
      return redirect('/labEvaluation/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4))
   if course.main.email==request.user.email:
      ok=0
   elif course.external.email==request.user.email:
      ok=1
   elif course.thirdExaminer.email==request.user.email:
      ok=2
   if ok==3:
      return redirect('/error')
   elif ok==0 and course.done==1:
      return redirect('/error')
   elif ok==1 and course.extDone==1:
      return redirect('/error')
   elif ok==2 and course.diff==0:
      return redirect('/error')
   elif ok==2 and course.diff==1 and course.thirdDone:
      return redirect('/error')
   mm=nonSem.objects.filter(dept=dept,session=session,semester=semester,course=course,teacher=ok)
   if not mm:
      for o in students:
         oo=nonSem(dept=dept,
            session=session,semester=semester,course=course,
            student=Student.objects.get(studentId=o.studentId),
            teacher=ok
         )
         oo.save()
   if 'save' in request.POST:
      for o,i in zip(request.POST.getlist('sem'),students):
         cc=nonSem.objects.get(dept=dept,session=session,semester=semester,course=course,
                                 student=Student.objects.get(studentId=i.studentId),
                                 teacher=ok)
         cc.final=Decimal(o)
         cc.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   if 'sub' in request.POST:
      if ok==0:
         course.done=1
         course.save()
      elif ok==1:
         course.extDone=1
         course.save()
      elif ok==2:
         course.thirdDone=1
         course.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)   
   if 'cancel' in request.POST:
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   me=nonSem.objects.filter(dept=dept,session=session,semester=semester,course=course,teacher=ok)
   cont={
      'marks':me,
      'course':course
   }
   return render(request,'sem.html',cont)
def labEvaluation(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   students=Student.objects.filter(dept=dept,session=session)
   ok=3
   if course.main.email==request.user.email:
      ok=0
   elif course.external.email==request.user.email:
      ok=1
   elif course.thirdExaminer.email==request.user.email:
      ok=2
   if ok==3:
      return redirect('/error')
   elif ok==0 and course.done==1:
      return redirect('/error')
   elif ok==1 and course.extDone==1:
      return redirect('/error')
   elif ok==2 and course.diff==0:
      return redirect('/error')
   elif ok==2 and course.diff==1 and course.thirdDone:
      return redirect('/error')
   mm=None
   if course.obe==0:
      mm=nonSem.objects.filter(dept=dept,session=session,semester=semester,course=course,teacher=ok)
   else:
      mm=Final.objects.filter(dept=dept,session=session,semester=semester,course=course,teacher=ok)
   if not mm:
      for o in students:
         if course.obe==0:
            oo=nonSem(dept=dept,
               session=session,semester=semester,course=course,
               student=Student.objects.get(studentId=o.studentId),
               teacher=ok
            )
            oo.save()
         else:
            oo=Final(
               dept=dept,session=session,semester=semester,course=course,
               student=Student.objects.get(studentId=o.studentId),
               teacher=ok
            )
            oo.save()
   if 'save' in request.POST:
      for o,i in zip(request.POST.getlist('sem'),students):
         if course.obe==0:
            cc=nonSem.objects.get(dept=dept,session=session,semester=semester,course=course,
                                    student=Student.objects.get(studentId=i.studentId),
                                    teacher=ok)
            cc.total=Decimal(o)
            cc.save()
         else:
            oo=Final.objects.get(
               dept=dept,session=session,semester=semester,course=course,
               student=Student.objects.get(studentId=i.studentId),
               teacher=ok
            )
            oo.total=Decimal(o)
            oo.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   if 'sub' in request.POST:
      if ok==0:
         course.done=1
         course.save()
      elif ok==1:
         course.extDone=1
         course.save()
      elif ok==2:
         course.thirdDone=1
         course.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)   
   if 'cancel' in request.POST:
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   me=None
   if course.obe==0:
      me=nonSem.objects.filter(dept=dept,session=session,semester=semester,course=course,teacher=ok)
   else:
      me=Final.objects.filter(dept=dept,session=session,semester=semester,course=course,teacher=ok)
   cont={
      'marks':me,
      'course':course
   }
   return render(request,'labEvaluation.html',cont)
def nonEvaluation(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   bb=int((int(id2)+1)/2)
   com=Committee.objects.get(dept=dept,session=session,comId=bb)
   comma=0
   if request.user.email==com.comChairman.email or request.user.email==com.comMember1.email or request.user.email==com.comMember2.email:
      comma=1
   if comma==0:
      return redirect('/error')
   cont=None
   if course.done==1 and course.extDone==1:
      cc=nonCombined.objects.filter(dept=dept,session=session,semester=semester,course=course)
      if not cc:
         for o in students:
            std=Student.objects.get(dept=dept,studentId=o.studentId)
            aa=nonBestOf.objects.get(dept=dept,session=session,semester=semester,course=course,student=std)
            bb=nonSem.objects.get(dept=dept,session=session,semester=semester,course=course,student=std,teacher=0)
            ff=nonSem.objects.get(dept=dept,session=session,semester=semester,course=course,student=std,teacher=1)
            cc=0
            if course.credit==3:
               cc=aa.tutorial+aa.attendance+((bb.final+ff.final)/2)
            else:
               cc=aa.tutorial+aa.attendance+aa.lab+aa.assignment+((bb.total+ff.total)/2)
            dif=0
            if course.credit==3:
               dif=abs(bb.final-ff.final)
            else:
               dif=abs(bb.total-ff.total)
            if dif>=12:
               course.diff=1
               course.save()
            dd=0
            if cc >= 80.0:
                dd = 4.00
            elif cc < 80.0 and cc >= 75.0:
                dd = 3.75
            elif cc < 75.0 and cc >= 70:
                dd = 3.50
            elif cc < 70 and cc >= 65.0:
                dd = 3.25
            elif cc < 65.0 and cc >= 60.0:
                dd = 3.00
            elif cc < 60.0 and cc >= 55.0:
                dd = 2.75
            elif cc < 55.0 and cc >= 50.0:
                dd = 2.50
            elif cc < 50.0 and cc >= 45.0:
                dd = 2.25
            elif cc < 45.0 and cc >= 40.00:
                dd = 2.00
            else:
             dd = 0.00
            jj=nonCombined(dept=dept,
               session=session,
               semester=semester,
               course=course,
               diff=dif,
               student=Student.objects.get(studentId=o.studentId),
               grade=dd
            )
            jj.save()
      elif course.diff==1 and course.thirdDone==1:
         for o in students:
            std=Student.objects.get(dept=dept,studentId=o.studentId)
            aa=nonBestOf.objects.get(dept=dept,session=session,semester=semester,course=course,student=std)
            bb=nonSem.objects.get(dept=dept,session=session,semester=semester,course=course,student=std,teacher=2)
            cc=0
            if course.credit==3:
               cc=aa.tutorial+aa.attendance+bb.final
            else:
               cc=aa.tutorial+aa.attendance+bb.total+aa.lab+aa.assignment
            jj=nonCombined.objects.get(dept=dept,
               session=session,
               semester=semester,
               course=course,
               student=Student.objects.get(studentId=o.studentId)
            )
            jj.third=cc
            dd=0
            if cc >= 80.0:
                dd = 4.00
            elif cc < 80.0 and cc >= 75.0:
                dd = 3.75
            elif cc < 75.0 and cc >= 70:
                dd = 3.50
            elif cc < 70 and cc >= 65.0:
                dd = 3.25
            elif cc < 65.0 and cc >= 60.0:
                dd = 3.00
            elif cc < 60.0 and cc >= 55.0:
                dd = 2.75
            elif cc < 55.0 and cc >= 50.0:
                dd = 2.50
            elif cc < 50.0 and cc >= 45.0:
                dd = 2.25
            elif cc < 45.0 and cc >= 40.00:
                dd = 2.00
            else:
             dd = 0.00
            jj.grade=dd
            jj.save() 
      if course.done==1 and course.extDone==1:
         if course.diff==1 and course.thirdDone==1:
            course.finDone=1
            course.save()
         elif course.diff==0:
            course.finDone=1
            course.save()  
      kk=nonCombined.objects.filter(dept=dept,session=session,semester=semester,course=course)
      cont={
         'marks':kk
      }
   else:
      messages.error(request,'Result is not ready yet!',extra_tags='ready')
   return render(request,'nonEvaluation.html',cont)
def semResults(request,id,id2,id3):
   dept=Department.objects.get(deptId=int(id3))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   courses=Course.objects.filter(dept=dept,session=session,semester=semester)
   students=Student.objects.filter(dept=dept,session=session).order_by()
   totalCredit=0
   flag=False
   cont=None
   aga=0
   baga=0
   for o in courses:
      if o.finDone==0:
         flag=True
      totalCredit+=o.credit
      if o.obe==1 and o.credit==3:
         aga+=1
      elif o.obe==1 and o.credit!=3:
         baga+=1
   if flag is False and totalCredit>0:
      semester.done=1
      semester.save()
      oo=semResult.objects.filter(dept=dept,session=session,semester=semester)
      if not oo:
         for o in students:
            grade=0
            std=Student.objects.get(dept=dept,studentId=o.studentId)
            ma=semResult(dept=dept,session=session,semester=semester,student=std)
            ma.save()
            for i in courses:
               crs=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=i.courseCode)
               if crs.obe==1:
                  cc=CombinedResult.objects.get(dept=dept,session=session,semester=semester,course=crs,student=std)
                  if crs.diff==0:
                     ma.finCLO1=Decimal(ma.finCLO1)+cc.finCLO1
                     ma.finCLO2=Decimal(ma.finCLO2)+cc.finCLO2
                     ma.finCLO3=Decimal(ma.finCLO3)+cc.finCLO3
                     ma.finCLO4=Decimal(ma.finCLO4)+cc.finCLO4
                     ma.finCLO5=Decimal(ma.finCLO5)+cc.finCLO5
                     ma.finCLO6=Decimal(ma.finCLO6)+cc.finCLO6
                     ma.save()
                     grade+=(cc.grade*crs.credit)
                  else:
                     ma.finCLO1=Decimal(ma.finCLO1)+cc.thirdFinCLO1
                     ma.finCLO2=Decimal(ma.finCLO2)+cc.thirdFinCLO2
                     ma.finCLO3=Decimal(ma.finCLO3)+cc.thirdFinCLO3
                     ma.finCLO4=Decimal(ma.finCLO4)+cc.thirdFinCLO4
                     ma.finCLO5=Decimal(ma.finCLO5)+cc.thirdFinCLO5
                     ma.finCLO6=Decimal(ma.finCLO6)+cc.thirdFinCLO6
                     ma.save()
                     grade+=(cc.grade*crs.credit)
               else:
                  cc=nonCombined.objects.get(dept=dept,session=session,semester=semester,course=crs,student=std)
                  grade+=(cc.grade*crs.credit)
                 
            ma.grade=(grade/totalCredit)
            ma.save()
      dk=semResult.objects.filter(dept=dept,session=session,semester=semester).order_by()
      totalPass=0
      totalFail=0
      rem={'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
      und={'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
      ana={'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
      ap= {'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
      ev= {'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
      cr= {'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
      remLabels=['100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
      undLabels=['100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
      anaLabels=['100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
      apLabels=[ '100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
      evLabels=[ '100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
      crLabels=[ '100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
      remData=[]
      undData=[]
      anaData=[]
      apData=[]
      evData=[]
      crData=[]
      tag=(aga*17+baga*5)
      cag=(aga*5+baga*5)
      for o in dk:
         if o.finCLO1>0:
            ok=math.ceil((o.finCLO1/(tag))*100)
            st=str(ok)
            if st[1]=='0':
               rem[st]+=1
            else:
               sa=st[0]+'0'
               rem[sa]+=1
         if o.finCLO2>0:
            ok=math.ceil((o.finCLO2/(tag))*100)
            st=str(ok)
            if st[1]=='0':
               und[st]+=1
            else:
               sa=st[0]+'0'
               und[sa]+=1
         if o.finCLO3>0:
            ok=math.ceil((o.finCLO3/(tag))*100)
            st=str(ok)
            if st[1]=='0':
               ap[st]+=1
            else:
               sa=st[0]+'0'
               ap[sa]+=1
         if o.finCLO4>0:
            ok=math.ceil((o.finCLO4/(tag))*100)
            st=str(ok)
            if st[1]=='0':
               ana[st]+=1
            else:
               sa=st[0]+'0'
               ana[sa]+=1
         if o.finCLO5>0:
            ok=math.ceil((o.finCLO5/(tag))*100)
            st=str(ok)
            if st[1]=='0':
               ev[st]+=1
            else:
               sa=st[0]+'0'
               ev[sa]+=1
         if o.finCLO6>0:
            ok=math.ceil((o.finCLO6/(cag))*100)
            st=str(ok)
            if st[1]=='0':
               cr[st]+=1
            else:
               sa=st[0]+'0'
               cr[sa]+=1
         if o.grade>0:
            totalPass+=1
         else:
            totalFail+=1
      for o in rem:
         remData.append(rem[o])
      for o in ana:
         anaData.append(ana[o])
      for o in ap:
         apData.append(ap[o])
      for o in und:
         undData.append(und[o])
      for o in ev:
         evData.append(ev[o])
      for o in cr:
         crData.append(cr[o])
      passRate=(totalPass/len(students))*100
      failRate=(totalFail/len(students))*100
      ss=''
      if id2==1:
         ss='1st Semester'
      elif id2==2:
         ss='2nd Semester'
      elif id2==3:
         ss='3rd Semester'
      else:
         ss=str(id2)+'th Semester'
      cont={
         'ss':ss,
         'no':len(students),
         'marks':dk,
         'totalPass':totalPass,
         'totalFail':totalFail,
         'passRate':passRate,
         'failRate':failRate,
         'remData':remData,
         'remLabels':remLabels,
         'undData':undData,
         'undLabels':undLabels,
         'apData':apData,
         'apLabels':apLabels,
         'anaData':anaData,
         'anaLabels':anaLabels,
         'evLabels':evLabels,
         'evData':evData,
         'crData':crData,
         'crLabels':crLabels
      }
   else:
      messages.error(request,'Result has not published yet!',extra_tags='ready')
   return render(request,'semResult.html',cont)
def dashboard(request):
   tea=Teacher.objects.filter(email=request.user.email)
   bea=Student.objects.filter(email=request.user.email)
   cea=Staff.objects.filter(email=request.user.email)
   if tea:
      return redirect('/teacher')
   if bea:
      return redirect('/student/'+str(bea[0].studentId)+'/'+str(bea[0].session.session)+'/'+str(bea[0].dept.deptId))
   if cea:
      return redirect('/staff')
def teacher(request):
   teacher=Teacher.objects.get(email=request.user.email)
   chairman=0
   if teacher.chairman==1:
      chairman=1
   dept=Department.objects.get(deptId=teacher.dept.deptId)
   print(request.user.email)
   main=Course.objects.filter(main=teacher,finDone=0)
   third=Course.objects.filter(thirdExaminer=teacher,finDone=0)
   if 'session' in request.POST:
      cont={
         'flag':1,
         'dept':dept.deptId,
         'chairman':chairman
      }
      return render(request,'teacher.html',cont)
   if 'createSession' in request.POST:
       messages.error(request,'OK',extra_tags='session')
   if 'create' in request.POST:
       ii=Session(dept=dept,session=(request.POST.get('id')))
       ii.save()
       session=Session.objects.filter(dept=dept)
       cont={
           'session':session,
           'chairman':chairman,
           'dept':dept.deptId
       }
       url='/createSession/'+str(dept.deptId)
       return redirect(url)
   if 'viewSession' in request.POST:
      ii=Session.objects.filter(dept=dept)
      cont={
         'session':ii,
         'chairman':chairman
      }
      url='/createSession/'+str(dept.deptId)
      return redirect(url)
   if 'createCom' in request.POST:
      cont={
         'flag':2,
         'chairman':chairman
      }
      return render(request,'teacher.html',cont)
   if 'createSem' in request.POST:
      cont={
         'flag':4,
         'chairman':chairman
      }
      return render(request,'teacher.html',cont)
   if 'createSemester' in request.POST:
      url='/semester/'+request.POST.get('semSession')+"/"+str(dept.deptId)
      return redirect(url)
   if 'createCommittee' in request.POST:
      url='/semester/'+request.POST.get('id')+"/"+str(dept.deptId)
      return redirect(url)
   if 'viewCom' in request.POST:
      cont={
         'flag':3,
         'chairman':chairman
      }
      return redirect('/performance/'+str(teacher.teacherId)+'/'+str(teacher.dept.deptId))
   if 'viewCommittee' in request.POST:
      url='/viewCom/'+request.POST.get('id')+"/"+str(dept.deptId)
      return redirect(url)
   if 'course' in request.POST:
      cont={
         'flag':5,
         'chairman':chairman
      }
      return render(request,'teacher.html',cont)
   if 'createCourse' in request.POST:
      url='/semester/'+request.POST.get('corSession')+"/"+str(dept.deptId)
      return redirect(url)
   if 'courseTeacher' in request.POST:
      course=Course.objects.filter(finDone=0,main=teacher)
      cont={
         'flag':6,
         'course':course,
         'chairman':chairman
      }
      return render(request,'teacher.html',cont)
   if 'dekho' in request.POST:
      dd=int(request.POST['year'])
      a=Course.objects.filter(dept=dept,semester__semester=dd*2-1,semester__done=0)|Course.objects.filter(dept=dept,semester__semester=dd*2,semester__done=0)
      ss=""
      if dd==1:
         ss="1st"
      elif dd==2:
         ss="2nd"
      elif dd==3:
         ss="3rd"
      elif dd==4:
         ss="4th"
      cont={
         'flag':9,
         'chairman':chairman,
         'a':a,
         'ss':ss
      }
      return render(request,'teacher.html',cont)
   if 'overview' in request.POST:
      cont={
         'flag':9,
         'chairman':chairman,
      }
      return render(request,'teacher.html',cont)
   if 'external' in request.POST:
      course=Course.objects.filter(finDone=0,external=teacher)
      cont={
         'flag':7,
         'course':course,
         'chairman':chairman
      }
      return render(request,'teacher.html',cont)
   if 'thirdExaminer' in request.POST:
      course=Course.objects.filter(finDone=0,thirdExaminer=teacher)
      cont={
         'flag':8,
         'course':course,
         'chairman':chairman
      }
      return render(request,'teacher.html',cont)
   cont={
      'main':main,
      'third':third,
      'flag':1,
      'dept':dept.deptId,
      'chairman':chairman
   }
   return render(request,'teacher.html',cont)
def viewCom(request,id,id2):
   dept=Department.objects.get(deptId=int(id2))
   session=Session.objects.get(dept=dept,session=int(id))
   cc=Committee.objects.filter(dept=dept,session=session).order_by('comId')
   cont={
      'com':cc
   }
   return render(request,'viewCom.html',cont)
def noti(request):
   oo=Message.objects.filter(teacher__email=request.user.email).order_by('-date')
   cc=Message.objects.filter(teacher__email=request.user.email,read=0)
   if 'mark' in request.POST:
      gg=Message.objects.get(teacher__email=request.user.email,msgId=request.POST.get('mark'))
      gg.read=1
      gg.save()
      return redirect('/noti')
   cont={
      'oo':oo,
      'len':len(cc)
   }
   return render(request,'noti.html',cont)
from django.db.models import Q
def student(request,id,id2,id3):
   dept=Department.objects.get(deptId=int(id3))
   session=Session.objects.get(session=int(id2),dept=dept)
   ff=Student.objects.get(studentId=int(id),dept=dept,session=session)
   dept=Department.objects.get(deptId=ff.dept.deptId)
   sems=Semester.objects.filter(dept=dept,
      session__session=ff.session.session,
      done=1
   ).order_by('semester')
   flag=0
   konta=1
   if request.user.email==ff.email:
      flag=1
   ass=Course.objects.filter(dept=ff.dept,session=ff.session,credit=1,tutDone=0)|Course.objects.filter(dept=ff.dept,session=ff.session,credit=2,tutDone=0)
   ca=ass.order_by('semester')
   if 'attendance' in request.POST:
      konta=2
      cont={
         'flag':flag,
         'konta':konta,
         'ass':ca,
         'sems':sems
      }
      return render(request,'student.html',cont)
   if 'overview' in request.POST:
      ar=[]
      seme=[]
      for o in sems:
         if o.semester==1:
            seme.append('1st Semester')
         elif o.semester==2:
            seme.append('2nd Semester')
         elif o.semester==3:
            seme.append('3rd Semester')
         else:
            seme.append(str(o.semester)+"th Semester")
         mo=Semester.objects.get(dept=dept,session=session,semester=o.semester)
         course=Course.objects.filter(dept=dept,session=session,semester=mo)
         ar.append(course)
      lrem=[]
      arem=[]
      hrem=[]
      lund=[]
      aund=[]
      hund=[]
      lana=[]
      hana=[]
      aana=[]
      lapp=[]
      happ=[]
      aapp=[]
      leva=[]
      aeva=[]
      heva=[]
      lcre=[]
      hcre=[]
      acre=[]
      for o in ar:
         ave=0
         afk=0
         low=200
         high=0
         for i in o:
            mo=Semester.objects.get(dept=dept,session=session,semester=i.semester.semester)
            cou=Course.objects.get(dept=dept,session=session,semester=mo,courseCode=i.courseCode)
            if cou.obe==1:
 
               ii=CombinedResult.objects.get(dept=dept,session=session,semester=mo,course=cou,student=ff)
               afk+=1
               jj=0
               tag=0
               if cou.credit==3:
                  tag=17
               else:
                  tag=5
               if cou.diff==0:
                  jj=math.ceil((ii.finCLO1/tag)*100)
               else:
                  jj=math.ceil((ii.thirdFinCLO1/tag)*100)
               low=min(jj,low)
               high=max(jj,high)
               ave+=jj
         ck=[]
         ave=math.ceil(ave/afk)
         lrem.append(low)
         hrem.append(high)
         arem.append(ave)
      for o in ar:
         ave=0
         afk=0
         low=200
         high=0
         for i in o:
            mo=Semester.objects.get(dept=dept,session=session,semester=i.semester.semester)
            cou=Course.objects.get(dept=dept,session=session,semester=mo,courseCode=i.courseCode)
            if cou.obe==1:
               ii=CombinedResult.objects.get(dept=dept,session=session,semester=mo,course=cou,student=ff)
               afk+=1
               jj=0
               tag=0
               if cou.credit==3:
                  tag=17
               else:
                  tag=5
               if cou.diff==0:
                  jj=math.ceil((ii.finCLO2/tag)*100)
               else:
                  jj=math.ceil((ii.thirdFinCLO2/tag)*100)
               low=min(jj,low)
               high=max(jj,high)
               ave+=jj
         ck=[]
         ave=math.ceil(ave/afk)
         lund.append(low)
         aund.append(ave)
         hund.append(high)
      for o in ar:
         ave=0
         afk=0
         low=200
         high=0
         for i in o:
            mo=Semester.objects.get(dept=dept,session=session,semester=i.semester.semester)
            cou=Course.objects.get(dept=dept,session=session,semester=mo,courseCode=i.courseCode)
            if cou.obe==1:
               ii=CombinedResult.objects.get(dept=dept,session=session,semester=mo,course=cou,student=ff)
               afk+=1
               jj=0
               tag=0
               if cou.credit==3:
                  tag=17
               else:
                  tag=5
               if cou.diff==0:
                  jj=math.ceil((ii.finCLO3/tag)*100)
               else:
                  jj=math.ceil((ii.thirdFinCLO3/tag)*100)
               low=min(jj,low)
               high=max(jj,high)
               ave+=jj
         ck=[]
         ave=math.ceil(ave/afk)
         lana.append(low)
         aana.append(ave)
         hana.append(high)
      for o in ar:
         ave=0
         afk=0
         low=200
         high=0
         for i in o:
            mo=Semester.objects.get(dept=dept,session=session,semester=i.semester.semester)
            cou=Course.objects.get(dept=dept,session=session,semester=mo,courseCode=i.courseCode)
            if cou.obe==1:
               ii=CombinedResult.objects.get(dept=dept,session=session,semester=mo,course=cou,student=ff)
               afk+=1
               jj=0
               tag=0
               if cou.credit==3:
                  tag=17
               else:
                  tag=5
               if cou.diff==0:
                  jj=math.ceil((ii.finCLO4/tag)*100)
               else:
                  jj=math.ceil((ii.thirdFinCLO4/tag)*100)
               low=min(jj,low)
               high=max(jj,high)
               ave+=jj
         ave=math.ceil(ave/afk)
         lapp.append(low)
         aapp.append(ave)
         happ.append(high)
      for o in ar:
         ave=0
         afk=0
         low=200
         high=0
         for i in o:
            mo=Semester.objects.get(dept=dept,session=session,semester=i.semester.semester)
            cou=Course.objects.get(dept=dept,session=session,semester=mo,courseCode=i.courseCode)
            if cou.obe==1:
               ii=CombinedResult.objects.get(dept=dept,session=session,semester=mo,course=cou,student=ff)
               afk+=1
               jj=0
               tag=0
               if cou.credit==3:
                  tag=17
               else:
                  tag=5
               if cou.diff==0:
                  jj=math.ceil((ii.finCLO5/tag)*100)
               else:
                  jj=math.ceil((ii.thirdFinCLO5/tag)*100)
               low=min(jj,low)
               high=max(jj,high)
               ave+=jj
         ave=math.ceil(ave/afk)
         leva.append(low)
         aeva.append(ave)
         heva.append(high)
      for o in ar:
         ave=0
         afk=0
         low=200
         high=0
         for i in o:
            mo=Semester.objects.get(dept=dept,session=session,semester=i.semester.semester)
            cou=Course.objects.get(dept=dept,session=session,semester=mo,courseCode=i.courseCode)
            if cou.obe==1:
               ii=CombinedResult.objects.get(dept=dept,session=session,semester=mo,course=cou,student=ff)
               afk+=1
               jj=0
               tag=0
               if cou.credit==3:
                  tag=17
               else:
                  tag=5
               if cou.diff==0:
                  jj=math.ceil((ii.finCLO6/5)*100)
               else:
                  jj=math.ceil((ii.thirdFinCLO6/5)*100)
               low=min(jj,low)
               high=max(jj,high)
               ave+=jj
         ave=math.ceil(ave/afk)
         lcre.append(low)
         acre.append(ave)
         hcre.append(high)
      konta=4
      cont={
         'flag':flag,
         'konta':konta,
         'ass':ca,
         'sems':sems,
         'lrem':lrem,
         'lund':lund,
         'lana':lana,
         'lapp':lapp,
         'leva':leva,
         'lcre':lcre,
         'arem':arem,
         'aund':aund,
         'aana':aana,
         'aapp':aapp,
         'aeva':aeva,
         'acre':acre,
         'hrem':hrem,
         'hund':hund,
         'hana':hana,
         'happ':happ,
         'heva':heva,
         'hcre':hcre,
         'seme':seme,
        
      }
      return render(request,'student.html',cont)
   if 'result' in request.POST:
      konta=1
      cont={
         'flag':flag,
         'konta':konta,
         'ass':ca,
         'sems':sems
      }
      return render(request,'student.html',cont)
   if 'assignment' in request.POST:
      konta=3
      ce=cieQA.objects.filter(dept=dept,session=session,on=1)
      se=semQA.objects.filter(dept=dept,session=session,on=1)
      print(ce)
      cont={
         'flag':flag,
         'konta':konta,
         'ass':ca,
         'sems':sems,
         'ce':ce,
         'se':se
      }
      return render(request,'student.html',cont)
   if 'sem' in request.POST:
      print(request.POST.get('seme'))
      obe=CombinedResult.objects.filter(dept=dept,
         session__session=ff.session.session,
         semester__semester=int(request.POST.get('seme')),
         student=ff
      )
      nonObe=nonCombined.objects.filter(dept=dept,
         session__session=ff.session.session,
         semester__semester=int(request.POST.get('seme')),
         student=ff
      )
      acc=semResult.objects.filter(dept=dept,
         session__session=ff.session.session,
         semester__semester=int(request.POST.get('seme')),
         student=ff
      )
      cont={
         'obe':obe,
         'nObe':nonObe,
         'acc':acc,
         'sems':sems,
         'ass':ca,
         'flag':flag,
         'konta':1
      }
      return render(request,'student.html',cont)
   if 'atta' in request.POST:
      sem=Semester.objects.get(dept=dept,session=session,semester=int(request.POST.get('semester')))
      cour=Course.objects.filter(dept=dept,session=session,semester=sem)
      atData=[]
      atLabels=[]
      for o in cour:
         atLabels.append(o.name)
         cc=Course.objects.get(dept=dept,session=session,semester=sem,courseCode=o.courseCode)
         att=indAttendance.objects.get(dept=dept,session=session,semester=sem,course=cc,student=None)
         ca=indAttendance.objects.filter(dept=dept,session=session,semester=sem,course=cc,student=ff)
         atData.append(math.ceil((len(ca)/att.present)*100))
      ss=""
      if sem.semester==1:
         ss='1st Semester'
      elif sem.semester==2:
         ss='2nd Semester'
      elif sem.semester==3:
         ss='3rd Semester'
      else:
         ss=str(sem.semester)+('th Semester')
      cont={
         'sems':sems,
         'ass':ca,
         'atLabels':atLabels,
         'flag':flag,
         'atData':atData,
         'konta':2,
         'ss':ss
      }
      return render(request,'student.html',cont)
   cont={
      'sems':sems,
      'ass':ca,
      'flag':flag,
      'konta':konta
   }
   return render(request,'student.html',cont)
def generate(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   if request.user.email!=course.main.email:
      return redirect('/error')
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   cont=None
   cn=0
   nn=CIE.objects.filter(dept=dept,session=session,semester=semester,course=course)
   for o in nn:
      cn=max(cn,o.no)
   if 'ok' in request.POST:
      limit=int(request.POST.get('limit'))
      course.selected=limit
      course.save()
      quer={}
      for o in students:
         k=1
         quer.__setitem__(o.studentId,{})
         while k<=cn:
            cc=CIE.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o.studentId),no=k)
            quer[o.studentId].__setitem__(cc.no,cc.total)
            k+=1
      for o in quer:
         sorted_dict=sorted(quer[o].items(), key = lambda x:x[1], reverse = True)
         quer[o]=sorted_dict
      for o in quer:
         dd=bestOf.objects.filter(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o))
         if not dd:
            aa=bestOf(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o))
            aa.save()
            ca=0
            for i,j in quer[o]:
               ca+=1
               if ca>limit:
                  break
               cc=CIE.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o),no=i)
               aa.CLO1+=cc.CLO1
               aa.CLO2+=cc.CLO2
               aa.CLO3+=cc.CLO3
               aa.CLO4+=cc.CLO4
               aa.CLO5+=cc.CLO5
               aa.CLO6+=cc.CLO6
               aa.save()
            aa.CLO1/=limit
            aa.CLO2/=limit
            aa.CLO3/=limit
            aa.CLO4/=limit
            aa.CLO5/=limit
            aa.CLO6/=limit
            aa.total=aa.CLO1+aa.CLO2+aa.CLO3+aa.CLO4+aa.CLO5+aa.CLO6
            aa.save()
         else:
            ca=0
            aa=bestOf.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o))
            aa.CLO1=0
            aa.CLO3=0
            aa.CLO4=0
            aa.CLO5=0
            aa.CLO6=0
            aa.CLO2=0
            for i,j in quer[o]:
               ca+=1
               if ca>limit:
                  break
               cc=CIE.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o),no=i)
               aa.CLO1+=cc.CLO1
               aa.CLO2+=cc.CLO2
               aa.CLO3+=cc.CLO3
               aa.CLO4+=cc.CLO4
               aa.CLO5+=cc.CLO5
               aa.CLO6+=cc.CLO6
               aa.save()
            aa.CLO1/=limit
            aa.CLO2/=limit
            aa.CLO3/=limit
            aa.CLO4/=limit
            aa.CLO5/=limit
            aa.CLO6/=limit
            aa.total=aa.CLO1+aa.CLO2+aa.CLO3+aa.CLO4+aa.CLO5+aa.CLO6
            aa.save()
      total=indAttendance.objects.get(dept=dept,session=session,semester=semester,course=course,student=None).present
      for o in students:
         cc=len(indAttendance.objects.filter(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(dept=dept,studentId=o.studentId)))
         dd=(cc/total)*100
         ok=bestOf.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(dept=dept,studentId=o.studentId))
         no=0
         if dd>=90.0:
            no=10
         elif dd>=85.0:
            no=9
         elif dd>=80.0:
            no=8
         elif dd>=75.0:
            no=7
         elif dd>=70:
            no=6
         elif dd>=65:
            no=7
         elif dd>=60:
            no=6
         elif dd>=55:
            no=5
         elif dd>=50:
            no=4
         elif dd>=45:
            no=3
         elif dd>=40:
            no=2
         else:
            no=1
         ok.attendance=no
         ok.total+=ok.attendance
         ok.save()
      if course.credit!=3:
         for o in students:
            cc=Student.objects.get(dept=dept,session=session,studentId=o.studentId)
            dd=indLab.objects.filter(dept=dept,session=session,semester=semester,course=course,student=cc)
            tot=0
            ca=0
            for i in dd:
               ca+=1
               tot+=i.marks
            tot/=ca
            tot=math.ceil(tot)
            ok=bestOf.objects.get(dept=dept,session=session,semester=semester,course=course,student=cc)
            ok.lab=tot
            ok.total+=ok.lab
            ok.save()
            dd=Assignment.objects.filter(dept=dept,session=session,semester=semester,course=course,student=cc)
            tot=0
            ca=0
            for i in dd:
               ca+=1
               tot+=i.marks
            tot/=ca
            tot=math.ceil(tot)
            ok.assignment=tot
            ok.total+=ok.assignment
            ok.save()
      ko=bestOf.objects.filter(dept=dept,session=session,semester=semester,course=course)
      cont={
         'cn':range(cn),
         'ko':ko,
         'course':course

      }
      return render(request,'generate.html',cont)   
   if course.tutDone==0:
    cont={
         'cn':range(cn),
         'course':course
      }
   else:
      ko=bestOf.objects.filter(dept=dept,session=session,semester=semester,course=course)
      cont={
         'course':course,
         'ko':ko
      }
   if 'publish' in request.POST:
      course.tutDone=1
      course.save()
      url='/generate/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)
      return redirect(url)
   if 'back' in request.POST:
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   return render(request,'generate.html',cont)
def nonGenerate(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   if request.user.email!=course.main.email:
      return redirect('/error')
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   cont=None
   cn=0
   nn=Tutorial.objects.filter(dept=dept,session=session,semester=semester,course=course)
   for o in nn:
      cn=max(cn,o.no)
   if 'ok' in request.POST:
      limit=int(request.POST.get('limit'))
      course.selected=limit
      course.save()
      quer={}
      for o in students:
         k=1
         quer.__setitem__(o.studentId,{})
         while k<=cn:
            cc=Tutorial.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o.studentId),no=k)
            quer[o.studentId].__setitem__(cc.no,cc.total)
            k+=1
      for o in quer:
         sorted_dict=sorted(quer[o].items(), key = lambda x:x[1], reverse = True)
         quer[o]=sorted_dict
      for o in quer:
         dd=nonBestOf.objects.filter(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o))
         if not dd:
            aa=nonBestOf(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o))
            aa.save()
            ca=0
            for i,j in quer[o]:
               ca+=1
               if ca>limit:
                  break
               cc=Tutorial.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o),no=i)
               aa.tutorial+=cc.tutorial
               aa.save()
            aa.tutorial/=limit
            aa.total=aa.tutorial
            aa.save()
         else:
            ca=0
            aa=nonBestOf.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o))
            aa.tutorial=0
            aa.total=0
            aa.save()
            for i,j in quer[o]:
               ca+=1
               if ca>limit:
                  break
               cc=Tutorial.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o),no=i)
               aa.tutorial+=cc.tutorial
               aa.save()
            aa.tutorial/=limit
            aa.total=aa.tutorial
            aa.save()
            
      total=indAttendance.objects.get(dept=dept,session=session,semester=semester,course=course,student=None).present
      for o in students:
         cc=len(indAttendance.objects.filter(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(dept=dept,studentId=o.studentId)))
         dd=(cc/total)*100
         ok=nonBestOf.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(dept=dept,studentId=o.studentId))
         no=0
         if dd>=90.0:
            no=10
         elif dd>=85.0:
            no=9
         elif dd>=80.0:
            no=8
         elif dd>=75.0:
            no=7
         elif dd>=70:
            no=6
         elif dd>=65:
            no=7
         elif dd>=60:
            no=6
         elif dd>=55:
            no=5
         elif dd>=50:
            no=4
         elif dd>=45:
            no=3
         elif dd>=40:
            no=2
         else:
            no=1
         ok.attendance=no
         ok.total+=ok.attendance
         ok.save()
      if course.credit!=3:
         for o in students:
            cc=Student.objects.get(dept=dept,session=session,studentId=o.studentId)
            dd=indLab.objects.filter(dept=dept,session=session,semester=semester,course=course,student=cc)
            tot=0
            ca=0
            for i in dd:
               ca+=1
               tot+=i.marks
            tot/=ca
            tot=math.ceil(tot)
            ok=nonBestOf.objects.get(dept=dept,session=session,semester=semester,course=course,student=cc)
            ok.lab=tot
            ok.total+=ok.lab
            ok.save()
            dd=Assignment.objects.filter(dept=dept,session=session,semester=semester,course=course,student=cc)
            tot=0
            ca=0
            for i in dd:
               ca+=1
               tot+=i.marks
            tot/=ca
            tot=math.ceil(tot)
            ok.assignment=tot
            ok.total+=ok.assignment
            ok.save()
      ko=nonBestOf.objects.filter(dept=dept,session=session,semester=semester,course=course)
      cont={
         'cn':range(cn),
         'ko':ko,
         'course':course

      }
      return render(request,'nonGenerate.html',cont)   
   if course.tutDone==0:
    cont={
         'cn':range(cn),
         'course':course
      }
   else:
      ko=nonBestOf.objects.filter(dept=dept,session=session,semester=semester,course=course)
      cont={
         'course':course,
         'ko':ko
      }
   if 'publish' in request.POST:
      course.tutDone=1
      course.save()
      url='/nonGenerate/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)
      return redirect(url)
   if 'back' in request.POST:
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   return render(request,'nonGenerate.html',cont)
def lab(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   today=datetime.datetime.now().date()
   if request.user.email!=course.main.email:
      return redirect('/error')
   elif course.tutDone==1:
      return redirect('/error')
   nn=indLab.objects.filter(dept=dept,session=session,semester=semester,course=course,date=today)
   if not nn:
      if 'evaluate' in request.POST:
         for o,i in zip(students,request.POST.getlist('lab')):
            ind=indLab(
               dept=dept,session=session,semester=semester,course=course,
               student=Student.objects.get(dept=dept,session=session,studentId=int(o.studentId)),
               marks=int(i),date=today
            )
            ind.save()
         url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
         return redirect(url)
   else:
         messages.error(request,'Evaluation is already completed for today. !',extra_tags='taken')
   if 'cancel' in  request.POST:
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   cont={
      'course':course,
      'students':students,
      'date':today
   }
   return render(request,'lab.html',cont)
def assignment(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   ff=False
   
   for o in students:
      if request.user.email==o.email:
         ff=True
   if request.user.email!=course.main.email and ff==False:
      return redirect('/error')
   if course.tutDone==1:
      return redirect('/error')
   jj=None
   if ff is False:
      jj=Assignment.objects.filter(dept=dept,session=session,semester=semester,course=course,student=None)
   else:
      jj=Assignment.objects.filter(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(dept=dept,session=session,email=request.user.email))
   cc=Assignment.objects.filter(dept=dept,session=session,semester=semester,course=course,student=None)
   main=False
   if request.user.email==course.main.email:
      main=True
   
   cont={
      'course':course,
      'ass':zip(jj,cc),
      'main':main
   }
   if 'create' in request.POST:
      messages.error(request,'oo',extra_tags='kk')
   if 'turn' in request.POST:
      today=datetime.datetime.now().date()
      print(today)
      cc=Assignment.objects.get(
         dept=dept,session=session,semester=semester,
         course=course,student=Student.objects.get(dept=dept,session=session,email=request.user.email),
         assignmentId=request.POST.get('turn')
      )
      if request.FILES.get('fil'):
         cc.fi=request.FILES.get('fil')
      if cc.date>=today:
         cc.status='Turned In'
      else:
         cc.status='Turned In Late'
      cc.save()
      return redirect('/assignment/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4))
   if 'grade' in request.POST:
      messages.error(request,'sodf',extra_tags='grade')
   if 'sth' in request.POST:
      iid=len(Assignment.objects.filter())+1
      bb=Assignment(
         assignmentId=iid,
         dept=dept,session=session,semester=semester,
         course=course,name=request.POST.get('name'),
            desc=request.POST.get('desc'),
            date=request.POST.get('date'),
            teaFi=request.FILES.get('jj')
      )
      bb.save()
      for o in students:
         cc=Assignment(
            assignmentId=iid,
            dept=dept,session=session,semester=semester,
            course=course,student=Student.objects.get(studentId=o.studentId),
            name=request.POST.get('name'),
            desc=request.POST.get('desc'),
            date=request.POST.get('date'),
            status='pending'
         )
         cc.save()
      return redirect('/assignment/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4))
   if 'cancelo' in request.POST:
      url='/indCourse/'+str(session.session)+'/'+str(semester.semester)+'/'+str(course.courseCode)+'/'+str(dept.deptId)      
      return redirect(url)
   if 'cancel' in request.POST:
      return redirect('/assignment/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4))
   return render(request,'assignment.html',cont)
def pdf_view(request,id):
  mail=Assignment.objects.get(assignmentId=int(id),student=None)
  filepath = os.path.join('media', str(mail.teaFi))
  return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def pdfs_view(request,id,id2,id3,id4):
  dept=Department.objects.get(deptId=int(id2))
  session=Session.objects.get(dept=dept,session=int(id3))
  student=Student.objects.get(dept=dept,session=session,studentId=int(id4))
  mail=Assignment.objects.get(dept=dept,session=session,assignmentId=int(id),student=student)
  filepath = os.path.join('media', str(mail.fi))
  return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def indAss(request,id):
   assignment=Assignment.objects.get(assignmentId=int(id),student=None)
   dept=Department.objects.get(deptId=assignment.dept.deptId)
   session=Session.objects.get(dept=dept,session=assignment.session.session)
   semester=Semester.objects.get(dept=dept,session=session,semester=assignment.semester.semester)
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=assignment.course.courseCode)
   ar=[]
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   for o in students:
      ass=Assignment.objects.get(
         dept=dept,session=session,semester=semester,course=course,
         student=Student.objects.get(studentId=o.studentId),
         assignmentId=int(id)
      )
      ar.append(ass)
   if 'dekha' in request.POST:
      return redirect('/pdfs/'+str(id)+'/'+str(dept.deptId)+'/'+str(session.session)+'/'+str(request.POST.get('dekha')))
   if 'cancel' in request.POST:
         url='/assignment/'+str(session.session)+'/'+str(semester.semester)+'/'+str(course.courseCode)+'/'+str(dept.deptId)      
         return redirect(url)
   if 'grading' in request.POST:
      for o,i  in zip(students,request.POST.getlist('marks')):
         cc=Assignment.objects.get(dept=dept,session=session,semester=semester,course=course,student=Student.objects.get(studentId=o.studentId),assignmentId=int(id))
         cc.marks=int(i)
         cc.save()
      url='/indCourse/'+str(session.session)+'/'+str(semester.semester)+'/'+str(course.courseCode)+'/'+str(dept.deptId)      
      return redirect(url)
   cont={
      'assignment':assignment,
      'ass':ar
   }
   return render(request,'indAss.html',cont)
def copo(request,id,id2,id3):
   dept=Department.objects.get(deptId=int(id3))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.filter(dept=dept,session=session,semester=semester)
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   if semester.done==1:
      for o in course:
        if o.obe==1:
         cc=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=o.courseCode)
         ar=[]
         average=[]
         jj=CombinedResult.objects.filter(dept=dept,session=session,semester=semester,course=cc)
         ave=0
         ff=[]
         jk=0
         if cc.credit==3:
            jk=17
         else:
            jk=5
         for o in jj:
            ko={}
            kk=o.finCLO1
            dd=math.ceil((o.finCLO1/jk)*100)
            ee=0
            if dd>=50:
               ee=3
            elif dd>=30:
               ee=2
            else:
               ee=1
            bb=copp.objects.filter(dept=dept,session=session,semester=semester,course=cc,student=Student.objects.get(studentId=o.student.studentId),co1=1)
            if not bb:
               ca=copp(
                  dept=dept,session=session,semester=semester,course=cc,
                  student=Student.objects.get(studentId=o.student.studentId),
                  co1=1,
                  marks=kk,
                  percentage=dd,
                  attained=ee
               )
               ca.save()
            ko.__setitem__(o.student,[kk,dd,ee])
            ff.append(ko)
            ave+=ee
         ar.append(ff)
         ff=[]
         ave=(ave/len(jj))
         average.append(ave)
         ave=0
         for o in jj:
            ko={}
            kk=o.finCLO2
            dd=math.ceil((o.finCLO2/jk)*100)
            ee=0
            if dd>=50:
               ee=3
            elif dd>=30:
               ee=2
            else:
               ee=1
            bb=copp.objects.filter(dept=dept,session=session,semester=semester,course=cc,student=Student.objects.get(studentId=o.student.studentId),co2=1)
            if not bb:
               ca=copp(
                  dept=dept,session=session,semester=semester,course=cc,
                  student=Student.objects.get(studentId=o.student.studentId),
                  co2=1,
                  marks=kk,
                  percentage=dd,
                  attained=ee
               )
               ca.save()
            ko.__setitem__(o.student,[kk,dd,ee])
            ff.append(ko)
            ave+=ee
         ar.append(ff)
         ff=[]
         ave=(ave/len(jj))
         average.append(ave)
         ave=0
         for o in jj:
            ko={}
            kk=o.finCLO3
            dd=math.ceil((o.finCLO3/jk)*100)
            ee=0
            if dd>=50:
               ee=3
            elif dd>=30:
               ee=2
            else:
               ee=1
            bb=copp.objects.filter(dept=dept,session=session,semester=semester,course=cc,student=Student.objects.get(studentId=o.student.studentId),co3=1)
            if not bb:
               ca=copp(
                  dept=dept,session=session,semester=semester,course=cc,
                  student=Student.objects.get(studentId=o.student.studentId),
                  co3=1,
                  marks=kk,
                  percentage=dd,
                  attained=ee
               )
               ca.save()
            ko.__setitem__(o.student,[kk,dd,ee])
            ff.append(ko)
            ave+=ee
         ar.append(ff)
         ff=[]
         ave=(ave/len(jj))
         average.append(ave)
         ave=0
         for o in jj:
            ko={}
            kk=o.finCLO4
            dd=math.ceil((o.finCLO4/jk)*100)
            ee=0
            if dd>=50:
               ee=3
            elif dd>=30:
               ee=2
            else:
               ee=1
            bb=copp.objects.filter(dept=dept,session=session,semester=semester,course=cc,student=Student.objects.get(studentId=o.student.studentId),co4=1)
            if not bb:
               ca=copp(
                  dept=dept,session=session,semester=semester,course=cc,
                  student=Student.objects.get(studentId=o.student.studentId),
                  co4=1,
                  marks=kk,
                  percentage=dd,
                  attained=ee
               )
               ca.save()
            ko.__setitem__(o.student,[kk,dd,ee])
            ff.append(ko)
            ave+=ee
         ar.append(ff)
         ff=[]
         ave=(ave/len(jj))
         average.append(ave)
         ave=0
         for o in jj:
            ko={}
            kk=o.finCLO5
            dd=math.ceil((o.finCLO5/jk)*100)
            ee=0
            if dd>=50:
               ee=3
            elif dd>=30:
               ee=2
            else:
               ee=1
            bb=copp.objects.filter(dept=dept,session=session,semester=semester,course=cc,student=Student.objects.get(studentId=o.student.studentId),co5=1)
            if not bb:
               ca=copp(
                  dept=dept,session=session,semester=semester,course=cc,
                  student=Student.objects.get(studentId=o.student.studentId),
                  co5=1,
                  marks=kk,
                  percentage=dd,
                  attained=ee
               )
               ca.save()
            ko.__setitem__(o.student,[kk,dd,ee])
            ff.append(ko)
            ave+=ee
         ar.append(ff)
         ff=[]
         ave=(ave/len(jj))
         average.append(ave)
         ave=0
         for o in jj:
            ko={}
            kk=o.finCLO6
            dd=math.ceil((o.finCLO6/5)*100)
            ee=0
            if dd>=50:
               ee=3
            elif dd>=30:
               ee=2
            else:
               ee=1
            ko.__setitem__(o.student,[kk,dd,ee])
            ff.append(ko)
            ave+=ee
         ar.append(ff)
         ff=[]
         ave=(ave/len(jj))
         average.append(ave)
      if 'dekha' in request.POST:
         ar=[]
         average=[]
         oka=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(request.POST.get('course')))
         ok=copp.objects.filter(dept=dept,session=session,semester=semester,course=oka,co1=1)
         cc=0
         for o in ok:
            cc+=o.attained
         cc/=len(ok)
         average.append(cc)
         ar.append(ok)
         ok=copp.objects.filter(dept=dept,session=session,semester=semester,course=oka,co2=1)
         cc=0
         for o in ok:
            cc+=o.attained
         cc/=len(ok)
         average.append(cc)
         ar.append(ok)
         ok=copp.objects.filter(dept=dept,session=session,semester=semester,course=oka,co3=1)
         cc=0
         for o in ok:
            cc+=o.attained
         cc/=len(ok)
         average.append(cc)
         ar.append(ok)
         ok=copp.objects.filter(dept=dept,session=session,semester=semester,course=oka,co4=1)
         cc=0
         for o in ok:
            cc+=o.attained
         cc/=len(ok)
         average.append(cc) 
         ar.append(ok)
         ok=copp.objects.filter(dept=dept,session=session,semester=semester,course=oka,co5=1)
         cc=0
         for o in ok:
            cc+=o.attained
         cc/=len(ok)
         average.append(cc)
         ar.append(ok)
         cont={
            'course':course,
        'session':session,
        'some':zip(ar,average,range(6)),
      'semester':semester,
      'dept':dept,
      'students':students
         }
         return render(request,'copo.html',cont)
      if 'stud' in request.POST:
            ar=[]
            ca=[]
            student=Student.objects.get(dept=dept,session=session,studentId=int(request.POST.get('stud')))
            for o in course:
             if o.obe==1:
               cc=copp.objects.filter(dept=dept,session=session,
                                   semester=semester,course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=o.courseCode),
                                   student=student)
               ca.append(o)
               ar.append(cc)
            messages.success(request,{'val':zip(ca,ar)},extra_tags='dokh')
      if 'ar' in request.POST:
         threshold=int(request.POST.get('thresh'))
         cc=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(request.POST.get('cor')))
         ar=[]
         ia=copp.objects.filter(
            dept=dept,session=session,semester=semester,course=cc,
            co1=1
         )
         cno=0
         cb=0
         kur=[]
         fur=[]
         dur=[]
         flag=False
         for i in ia:
            if i.percentage<threshold:
               flag=True
            if i.percentage>=threshold:
               cno+=1
         if flag is True:
            kur.append('No')
         else:
            kur.append('Yes')
         fur.append(cno)
         dur.append((cno/len(ia))*100)
         ar.append(kur)   
         ia=copp.objects.filter(
            dept=dept,session=session,semester=semester,course=cc,
            co2=1
         )
         cno=0
         cb=0
         flag=False
         for i in ia:
            if i.percentage<threshold:
               flag=True
            if i.percentage>=threshold:
               cno+=1
         if flag is True:
            kur.append('No')
         else:
            kur.append('Yes')
         fur.append(cno)
         dur.append((cno/len(ia))*100)
         ar.append(kur)   
         ia=copp.objects.filter(
            dept=dept,session=session,semester=semester,course=cc,
            co3=1
         )
         cno=0
         cb=0
         flag=False
         for i in ia:
            if i.percentage<threshold:
               flag=True
            if i.percentage>=threshold:
               cno+=1
         if flag is True:
            kur.append('No')
         else:
            kur.append('Yes')
         fur.append(cno)
         dur.append((cno/len(ia))*100)
         ar.append(kur)   
         ia=copp.objects.filter(
            dept=dept,session=session,semester=semester,course=cc,
            co4=1
         )
         cno=0
         cb=0
         flag=False
         for i in ia:
            if i.percentage<threshold:
               flag=True
            if i.percentage>=threshold:
               cno+=1
         if flag is True:
            kur.append('No')
         else:
            kur.append('Yes')
         fur.append(cno)
         dur.append((cno/len(ia))*100)
         ar.append(kur)   
         ia=copp.objects.filter(
            dept=dept,session=session,semester=semester,course=cc,
            co5=1
         )
         cno=0
         cb=0
         flag=False
         for i in ia:
            if i.percentage<threshold:
               flag=True
            if i.percentage>=threshold:
               cno+=1
         if flag is True:
            kur.append('No')
         else:
            kur.append('Yes')
         fur.append(cno)
         dur.append(((cno/len(ia))*100))
         print(kur)
         cont={
            'course':course,
            'session':session,
            'semester':semester,
            'dept':dept,
            'students':students,
            'kur':kur,
            'fur':fur,
            'dur':dur,
            'gur':threshold
         }
         return render(request,'copo.html',cont)
   else:
      messages.error(request,"Semester Result Has not been published yet !",extra_tags='naire')
   cont={
      'course':course,
      'session':session,
      'semester':semester,
      'dept':dept,
      'students':students
   }
   return render(request,'copo.html',cont)
def performance(request,id,id2):
   dept=Department.objects.get(deptId=int(id2))
   teacher=Teacher.objects.get(teacherId=int(id),dept=dept)
   semester=Semester.objects.filter(dept=dept,done=1)
   ar=[]
   for o in semester:
      cc=Course.objects.filter(dept=dept,semester=o,session=o.session,main=teacher)
      if cc:
         for i in cc:
            ar.append(i)
   rem={'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
   und={'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
   ana={'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
   ap= {'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
   ev= {'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
   cr= {'100':0,'90':0,'80':0,'70':0,'60':0,'50':0,'40':0,'30':0,'20':0,'10':0}
   remLabels=['100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
   undLabels=['100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
   anaLabels=['100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
   apLabels=[ '100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
   evLabels=[ '100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
   crLabels=[ '100%','90-99%','80-89%','70-79%','60-69%','50-59%','40-49%','30-39%','20-29%','10-19%']
   remData=[]
   undData=[]
   anaData=[]
   apData=[]
   evData=[]
   crData=[]
   kur={'co1':0,'co2':0,'co3':0,'co4':0,'co5':0,'co6':0}
   kn=0
   for o in ar:
      course=Course.objects.get(dept=dept,semester=o.semester,session=o.session,courseCode=o.courseCode,obe=1)
      combo=CombinedResult.objects.filter(dept=dept,semester=o.semester,session=o.session,course=course)
      tag=0
      kn+=len(combo)
      if course.credit==3:
         tag=17
      else:
         tag=5
      for o in combo:
         if course.diff==0:
            if o.finCLO1>0:
               ok=math.ceil((o.finCLO1/(tag))*100)
               kur['co1']+=ok
               st=str(ok)
               if st[1]=='0':
                  rem[st]+=1
               else:
                  sa=st[0]+'0'
                  rem[sa]+=1
            if o.finCLO2>0:
               ok=math.ceil((o.finCLO2/(tag))*100)
               kur['co2']+=ok
               st=str(ok)
               if st[1]=='0':
                  und[st]+=1
               else:
                  sa=st[0]+'0'
                  und[sa]+=1
            if o.finCLO3>0:
               ok=math.ceil((o.finCLO3/(tag))*100)
               kur['co3']+=ok
               st=str(ok)
               if st[1]=='0':
                  ap[st]+=1
               else:
                  sa=st[0]+'0'
                  ap[sa]+=1
            if o.finCLO4>0:
               ok=math.ceil((o.finCLO3/(tag))*100)
               kur['co4']+=ok
               st=str(ok)
               if st[1]=='0':
                  ana[st]+=1
               else:
                  sa=st[0]+'0'
                  ana[sa]+=1
            if o.finCLO5>0:
               ok=math.ceil((o.finCLO5/(tag))*100)
               kur['co5']+=ok
               st=str(ok)
               if st[1]=='0':
                  ev[st]+=1
               else:
                  sa=st[0]+'0'
                  ev[sa]+=1
            if o.finCLO6>0:
               ok=math.ceil((o.finCLO6/(5))*100)
               st=str(ok)
               kur['co6']+=ok
               if st[1]=='0':
                  cr[st]+=1
               else:
                  sa=st[0]+'0'
                  cr[sa]+=1
         else:
            if o.thirdFinCLO1>0:
               ok=math.ceil((o.thirdFinCLO1/(tag))*100)
               st=str(ok)
               kur['co1']+=ok
               if st[1]=='0':
                  rem[st]+=1
               else:
                  sa=st[0]+'0'
                  rem[sa]+=1
            if o.thirdFinCLO2>0:
               ok=math.ceil((o.thirdFinCLO2/(tag))*100)
               st=str(ok)
               kur['co2']+=ok
               if st[1]=='0':
                  und[st]+=1
               else:
                  sa=st[0]+'0'
                  und[sa]+=1
            if o.thirdFinCLO3>0:
               ok=math.ceil((o.thirdFinCLO3/(tag))*100)
               st=str(ok)
               kur['co3']+=ok
               if st[1]=='0':
                  ap[st]+=1
               else:
                  sa=st[0]+'0'
                  ap[sa]+=1
            if o.thirdFinCLO4>0:
               ok=math.ceil((o.thirdFinCLO4/(tag))*100)
               st=str(ok)
               kur['co4']+=ok
               if st[1]=='0':
                  ana[st]+=1
               else:
                  sa=st[0]+'0'
                  ana[sa]+=1
            if o.thirdFinCLO5>0:
               ok=math.ceil((o.thirdFinCLO5/(tag))*100)
               st=str(ok)
               kur['co5']+=ok
               if st[1]=='0':
                  ev[st]+=1
               else:
                  sa=st[0]+'0'
                  ev[sa]+=1
            if o.thirdFinCLO6>0:
               ok=math.ceil((o.thirdFinCLO6/(5))*100)
               st=str(ok)
               kur['co6']+=ok
               if st[1]=='0':
                  cr[st]+=1
               else:
                  sa=st[0]+'0'
                  cr[sa]+=1
   for o in kur:
      if kn!=0:
         kur[o]=math.ceil(kur[o]/kn)
   for o in rem:
      remData.append(rem[o])
   for o in ana:
      anaData.append(ana[o])
   for o in ap:
      apData.append(ap[o])
   for o in und:
      undData.append(und[o])
   for o in ev:
      evData.append(ev[o])
   for o in cr:
      crData.append(cr[o])
   jar=[]
   for o in kur:
      jar.append(kur[o])
   jarlabels=['Remember','Understand','Apply','Analyze','Evaluate','Create']
   cont={
      'jar':jar,
      'teacher':teacher,
      'jarLabels':jarlabels,
         'remData':remData,
         'remLabels':remLabels,
         'undData':undData,
         'undLabels':undLabels,
         'apData':apData,
         'apLabels':apLabels,
         'anaData':anaData,
         'anaLabels':anaLabels,
         'evLabels':evLabels,
         'evData':evData,
         'crData':crData,
         'crLabels':crLabels
   }
   return render(request,'performance.html',cont)
def results(request):
   depts=Department.objects.filter()
   cont={
      'depts':depts
   }
   return render(request,'results.html',cont)
def deptSession(request,id):
   dept=Department.objects.get(deptId=int(id))
   sessions=Session.objects.filter(dept__deptId=int(id))
   cont={'sessions':sessions}
   return render(request,'deptSession.html',cont)
def deptResult(request,id,id2):
   dept=Department.objects.get(deptId=int(id))
   session=Session.objects.get(dept=dept,session=int(id2))
   sems=Semester.objects.filter(dept=dept,session=session,done=1)
   cont={'oo':sems}
   return render(request,'deptResult.html',cont)
def deptSem(request,id,id2,id3):
   dept=Department.objects.get(deptId=int(id))
   session=Session.objects.get(dept=dept,session=int(id2))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id3))
   sems=semResult.objects.filter(dept=dept,session=session,semester=semester)
   ss=""
   id3=int(id3)
   if id3==1:
      ss="1st Semester"
   elif id3==2:
      ss="2nd Semester"
   elif id3==3:
      ss="3rd Semester"
   else:
      ss=str(id3)+"th Semester"
   cont={'oo':sems,"ss":ss}
   return render(request,'deptSem.html',cont)
def staff(request):
   staff=Staff.objects.get(email=request.user.email)
   dept=Department.objects.get(deptId=staff.dept.deptId)
   students=Student.objects.filter(dept=dept)
   teachers=Teacher.objects.filter(dept=dept)
   session=Session.objects.filter(dept=dept)
   courses=Course.objects.filter(dept=dept,session=None,semester=None)
   if 'session' in request.POST:
      ses=Session.objects.get(dept=dept,session=int(request.POST['ind']))
      studs=Student.objects.filter(dept=dept,session=ses)
      
      cont={
              'students':students,
      'teachers':teachers,
      'std':len(students),
      'tea':len(teachers),
      'session':session,
      'cour':len(courses),
      'courses':courses,
      'studs':studs
      }
      return render(request,'staff.html',cont)
   if 'action' in request.POST:
      st=Student.objects.get(email=request.POST['action'])
      st.delete()
      return redirect('/staff')
   if 'addTea' in request.POST:
      tea=Teacher(
         dept=dept,
         name=request.POST['name'],
         teacherId=request.POST['id'],
         email=request.POST['email']
      )
      tea.save()
      return redirect('/staff')
   if 'addStud' in request.POST:
      ses=Session.objects.get(dept=dept,session=int(request.POST['addSession']))
      stud=Student(
         dept=dept,
         session=ses,
         name=request.POST['name'],
         studentId=request.POST['id'],
         email=request.POST['email']
      )
      stud.save()
      return redirect('/staff')
   if 'addCourse' in request.POST:
      obe=0
      if request.POST['obe']=='on':
         obe=1
      cour=Course(
         dept=dept,
         name=request.POST['name'],
         courseCode=request.POST['code'],
         credit=request.POST['credit'],
         obe=obe
      )
      cour.save()
      return redirect('/staff')
   cont={
      'students':students,
      'teachers':teachers,
      'std':len(students),
      'tea':len(teachers),
      'session':session,
      'cour':len(courses),
      'courses':courses

   }
   return render(request,'staff.html',cont)
def cieQuestions(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   tea=Teacher.objects.filter(email=request.user.email)
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   da=cieQA.objects.filter(dept=dept,session=session,semester=semester,course=course)
   for o in da:
      if o.start is not None:
         startH=o.start.hour
         startM=o.start.minute
         startS=o.start.second
         nowH=datetime.datetime.now().hour
         nowM=datetime.datetime.now().minute
         nowS=datetime.datetime.now().second
         startT=startH*3600+startM*60+startS
         nowT=nowH*3600+nowM*60+nowS
         dd=o.duration*60
         ee=nowT-startT
         ff=dd-ee
         if ff<0:
            aa=cieQA.objects.get(dept=dept,session=session,semester=semester,course=course,no=o.no)
            aa.on=2
            aa.save()
   if not tea or tea[0]!=course.main:
      return redirect('/error')
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   if course.done==1:
      return redirect('/error')
   if 'save' in request.POST:
      dd=cieQA.objects.filter(dept=dept,session=session,semester=semester,course=course)
      ii=cieQA(
         dept=dept,
         session=session,
         semester=semester,
         course=course,
         no=len(dd)+1,
         ques=request.FILES.get('ques'),
         duration=request.POST.get('duration')
      )
      ii.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   if 'start' in request.POST:
      ea=cieQA.objects.get(dept=dept,session=session,semester=semester,course=course,no=int(request.POST.get('start')))
      ea.start=datetime.datetime.now()
      ea.on=1
      ea.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
      
   aa=cieQA.objects.filter(dept=dept,session=session,semester=semester,course=course)
   cont={
      'aa':aa,
      'course':course.name,

   }
   return render(request,'cieQuestions.html',cont)
def virtual(request,id,id1,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id3))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id1))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id2))
   student=Student.objects.get(email=request.user.email)
   cie=cieQA.objects.get(dept=dept,session=session,semester=semester,course=course,no=int(id4))
   ea=cieQ.objects.filter(dept=dept,session=session,semester=semester,course=course,student=student,no=cie.no)
   if ea:
      return redirect('/error')
   startH=cie.start.hour
   startM=cie.start.minute
   startS=cie.start.second
   nowH=datetime.datetime.now().hour
   nowM=datetime.datetime.now().minute
   nowS=datetime.datetime.now().second
   startT=startH*3600+startM*60+startS
   nowT=nowH*3600+nowM*60+nowS
   dd=cie.duration*60
   ee=nowT-startT
   ff=dd-ee
   if ff<0:
      cie.on=2
      cie.save()
      return redirect('/')
   hour=int(ff/3600)
   ff-=(hour*3600)
   minute=int(ff/60)
   ff-=(minute*60)
   second=ff
   if 'save' in request.POST:
      if ff<0:
         cie.on=2
         cie.save()
         return redirect('/')
      ii=cieQ(
         dept=dept,
         session=session,
         semester=semester,
         course=course,
         student=student,
         no=cie.no,
         clo1=request.FILES.get('clo1'),
         clo2=request.FILES.get('clo2'),
         clo3=request.FILES.get('clo3'),
         clo4=request.FILES.get('clo4'),
         clo5=request.FILES.get('clo5'),
         clo6=request.FILES.get('clo6'),
      ) 
      ii.save()
      return redirect('/')
   if 'question' in request.POST:
      filepath = os.path.join('media', str(cie.ques))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   cont={
      'ques':cie.ques,
      'course':course.name,
      'hour':hour,
      'minute':minute,
      'second':second
   }
   return render(request,'virtual.html',cont)
def semQuestions(request,id,id2,id3,id4):
   dept=Department.objects.get(deptId=int(id4))
   tea=Teacher.objects.filter(email=request.user.email)
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id2))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id3))
   da=semQA.objects.filter(dept=dept,session=session,semester=semester,course=course)
   ok=0
   if da:
      ok=1
   for o in da:
      if o.start is not None:
         startH=o.start.hour
         startM=o.start.minute
         startS=o.start.second
         nowH=datetime.datetime.now().hour
         nowM=datetime.datetime.now().minute
         nowS=datetime.datetime.now().second
         startT=startH*3600+startM*60+startS
         nowT=nowH*3600+nowM*60+nowS
         dd=o.duration*60
         ee=nowT-startT
         ff=dd-ee
         if ff<0:
            aa=semQA.objects.get(dept=dept,session=session,semester=semester,course=course)
            aa.on=2
            aa.save()
   if not tea or tea[0]!=course.main:
      return redirect('/error')
   students=Student.objects.filter(dept=dept,session=session).order_by('studentId')
   if course.done==1:
      return redirect('/error')
   if 'save' in request.POST:
      ii=semQA(
         dept=dept,
         session=session,
         semester=semester,
         course=course,
         ques=request.FILES.get('ques'),
         duration=request.POST.get('duration')
      )
      ii.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
   if 'start' in request.POST:
      ea=semQA.objects.get(dept=dept,session=session,semester=semester,course=course)
      ea.start=datetime.datetime.now()
      ea.on=1
      ea.save()
      url='/indCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)+'/'+str(id4)      
      return redirect(url)
      
   aa=semQA.objects.filter(dept=dept,session=session,semester=semester,course=course)
   cont={
      'aa':aa,
      'course':course.name,
      'ok':ok

   }
   return render(request,'semQuestions.html',cont)
def virtualSem(request,id,id1,id2,id3):
   dept=Department.objects.get(deptId=int(id3))
   session=Session.objects.get(dept=dept,session=int(id))
   semester=Semester.objects.get(dept=dept,session=session,semester=int(id1))
   course=Course.objects.get(dept=dept,session=session,semester=semester,courseCode=int(id2))
   student=Student.objects.get(email=request.user.email)
   sem=semQA.objects.get(dept=dept,session=session,semester=semester,course=course)
   ea=semQ.objects.filter(dept=dept,session=session,semester=semester,course=course,student=student)
   if ea:
      return redirect('/error')
   startH=sem.start.hour
   startM=sem.start.minute
   startS=sem.start.second
   nowH=datetime.datetime.now().hour
   nowM=datetime.datetime.now().minute
   nowS=datetime.datetime.now().second
   startT=startH*3600+startM*60+startS
   nowT=nowH*3600+nowM*60+nowS
   dd=sem.duration*60
   ee=nowT-startT
   ff=dd-ee
   if ff<0:
      sem.on=2
      sem.save()
      return redirect('/')
   hour=int(ff/3600)
   ff-=(hour*3600)
   minute=int(ff/60)
   ff-=(minute*60)
   second=ff
   if 'save' in request.POST:
      if ff<0:
         sem.on=2
         sem.save()
         return redirect('/')
      ii=semQ(
         dept=dept,
         session=session,
         semester=semester,
         course=course,
         student=student,
         clo1=request.FILES.get('clo1'),
         clo2=request.FILES.get('clo2'),
         clo3=request.FILES.get('clo3'),
         clo4=request.FILES.get('clo4'),
         clo5=request.FILES.get('clo5'),
      ) 
      ii.save()
      return redirect('/')
   if 'question' in request.POST:
      filepath = os.path.join('media', str(sem.ques))
      return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
   cont={
      'ques':sem.ques,
      'course':course.name,
      'hour':hour,
      'minute':minute,
      'second':second
   }
   return render(request,'virtualSem.html',cont)