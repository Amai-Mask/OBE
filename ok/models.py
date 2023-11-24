from django.db import models
import uuid
class Department(models.Model):
   name=models.CharField(max_length=100,null=True)
   deptId=models.IntegerField(null=True)
   def __str__(self):
      return str(self.name+" - "+str(self.deptId))
class Session(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.IntegerField(default=0)
    def __str__(self):
        return str(str(self.dept.name)+" - "+str(self.session))
class Staff(models.Model):
      dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
      name=models.CharField(max_length=40,blank=True,null=True)
      staffId=models.IntegerField(unique=True,blank=True,null=True)
      username=models.CharField(max_length=40,null=True,blank=True)
      email=models.EmailField(max_length=30,blank=True)
      password=models.CharField(max_length=15,blank=True)
      def __str__(self):
        return str(str(self.dept.name)+" - "+str(self.staffId))
class Student(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=40,blank=True,null=True)
    studentId=models.IntegerField(unique=True)
    username=models.CharField(max_length=40,null=True,blank=True)
    email=models.EmailField(max_length=30,blank=True)
    password=models.CharField(max_length=15,blank=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    image=models.ImageField(blank=True,null=True)
    def __str__(self):
        return str(self.dept.name+" - "+str(self.studentId))
class Teacher(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    chairman=models.IntegerField(default=0)
    teacherId=models.IntegerField(unique=True,blank=True,null=True)
    name=models.CharField(max_length=40,blank=True,null=True)
    username=models.CharField(max_length=40,null=True,blank=True)
    email=models.EmailField(max_length=40,blank=True)
    password=models.CharField(max_length=40,blank=True)
    image=models.ImageField(blank=True,null=True)
    chairman=models.IntegerField(default=0)
    def __str__(self):
        return str(self.dept.name+" - "+self.name)
class Committee(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True,blank=True)
    comId=models.IntegerField(null=True)
    comChairman=models.ForeignKey('Teacher',related_name='comChairman',on_delete=models.CASCADE,blank=True,null=True)
    comMember1=models.ForeignKey('Teacher',related_name='comMember1',on_delete=models.CASCADE,blank=True,null=True)
    comMember2=models.ForeignKey('Teacher',related_name='comMember2',on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return str(str(self.dept)+" - "+str(self.session)+" - "+str(self.comId))
class Semester(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.IntegerField(blank=True)
    done=models.IntegerField(default=0)
    def __str__(self):
        return str(self.dept.name+" - "+str(self.session)+str(" - "+str(self.semester)))
class Course(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    student=models.ManyToManyField(Student,null=True,blank=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True,blank=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True,blank=True)
    credit=models.IntegerField(default=0,blank=True)
    name=models.CharField(max_length=40,blank=True)
    courseCode=models.IntegerField(blank=True)
    done=models.IntegerField(default=0)
    obe=models.IntegerField(default=0)
    extDone=models.IntegerField(default=0)
    diff=models.IntegerField(default=0)
    thirdDone=models.IntegerField(default=0)
    tutDone=models.IntegerField(default=0)
    selected=models.IntegerField(default=0)
    finDone=models.IntegerField(default=0)
    thirdExaminer=models.ForeignKey('Teacher',related_name='thirdExaminer',on_delete=models.CASCADE,blank=True,null=True)
    main=models.ForeignKey('Teacher',related_name='main',on_delete=models.CASCADE,blank=True,null=True)
    external=models.ForeignKey('Teacher',related_name='external',on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return str(str(self.dept.name)+" - "+str(self.semester)+str(" - "+self.name))
class CIE(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    no=models.IntegerField(default=0)
    CLO1=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    CLO2=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    CLO3=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    CLO4=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    CLO5=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    CLO6=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    total=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    attendance=models.IntegerField(null=True,default=0)
    def __str__(self):
        return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode)+" - "+str(self.student.studentId))
class Final(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    teacher=models.IntegerField(default=0)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    semCLO1=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    semCLO2=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    semCLO3=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    semCLO4=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    semCLO5=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    total=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    def __str__(self):
     return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode)+" - "+str(self.student.studentId))
class CombinedResult(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    diff=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO1=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO2=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO3=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO4=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO5=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO6=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    thirdFinCLO1=models.IntegerField(default=0)
    thirdFinCLO2=models.IntegerField(default=0)
    thirdFinCLO3=models.IntegerField(default=0)
    thirdFinCLO4=models.IntegerField(default=0)
    thirdFinCLO5=models.IntegerField(default=0)
    thirdFinCLO6=models.IntegerField(default=0)
    total=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.00)
    thirdTotal=models.IntegerField(default=0)
    grade=models.DecimalField(max_digits=3,decimal_places=2,null=True,default=0.00)
    def __str__(self):
     return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode)+" - "+str(self.student.studentId)) 
class Tutorial(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    no=models.IntegerField(default=0)
    tutorial=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    total=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    attendance=models.IntegerField(default=0)
    def __str__(self):
     return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode)+" - "+str(self.student.studentId)) 
class nonSem(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    teacher=models.IntegerField(default=0)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    final=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    total=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    def __str__(self):
     return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode)+" - "+str(self.student.studentId)) 
class nonCombined(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    diff=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    third=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    grade=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    def __str__(self):
     return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode)+" - "+str(self.student.studentId)) 

class semResult(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    finCLO1=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO2=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO3=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO4=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO5=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    finCLO6=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0.0)
    grade=models.DecimalField(max_digits=3,decimal_places=2,null=True,default=0.00)
    def __str__(self):
     return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.student.studentId)) 
class Message(models.Model):
   msgId=models.IntegerField(default=0)
   teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
   text=models.TextField(max_length=400,null=True)
   read=models.IntegerField(default=0)
   date=models.DateTimeField(null=True,blank=True)
   def __str__(self):
      return str(self.date)
class indAttendance(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    present=models.IntegerField(default=0)
    def __str__(self):
       return str(str(self.dept.name)+" - "+str(self.session.session)+" - "+str(self.semester.semester)+" - "+str(self.course.name))
class bestOf(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    lab=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    CLO1=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    CLO2=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    CLO3=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    CLO4=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    CLO5=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    CLO6=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    assignment=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    total=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    attendance=models.IntegerField(default=0)
    def __str__(self):
       return str(str(self.dept.name)+" - "+str(self.session.session)+" - "+str(self.semester.semester)+" - "+str(self.course.name)+" - "+str(self.student.studentId))
class nonBestOf(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    assignment=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    lab=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    tutorial=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    total=models.DecimalField(max_digits=5,decimal_places=2,null=True,default=0)
    attendance=models.IntegerField(default=0)
    def __str__(self):
       return str(str(self.dept.name)+" - "+str(self.session.session)+" - "+str(self.semester.semester)+" - "+str(self.course.name)+" - "+str(self.student.studentId))
class indLab(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    marks=models.IntegerField(default=0)
    def __str__(self):
       return str(str(self.dept.name)+" - "+str(self.session.session)+" - "+str(self.semester.semester)+" - "+str(self.course.name))
class Assignment(models.Model):
    assignmentId=models.IntegerField(null=True)
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100,null=True)
    desc=models.TextField(max_length=1000,null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    fi=models.FileField(upload_to='',null=True)
    date=models.DateField(null=True)
    marks=models.IntegerField(default=0)
    teaFi=models.FileField(upload_to='',null=True)
    status=models.CharField(max_length=100,null=True,default='pending')
    def __str__(self):
       return str(str(self.dept.name)+" - "+str(self.session.session)+" - "+str(self.semester.semester)+" - "+str(self.course.name))
class copp(models.Model):
   co1=models.IntegerField(default=0)
   co2=models.IntegerField(default=0)
   co3=models.IntegerField(default=0)
   co4=models.IntegerField(default=0)
   co5=models.IntegerField(default=0)
   session=models.ForeignKey(Session,on_delete=models.CASCADE)
   semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
   dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
   course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
   student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
   percentage=models.IntegerField(null=True,default=0)
   marks=models.DecimalField(max_digits=5,decimal_places=2,null=True)
   attained=models.IntegerField(default=0)
   def __str__(self):
      return str(str(self.dept))
class cieQQ(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    no=models.IntegerField(default=0)
    ques=models.FileField(upload_to='',null=True)
    duration=models.IntegerField(default=0)
    start=models.DateTimeField(null=True,blank=True)
    on=models.IntegerField(default=0)
    def __str__(self):
        return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode))
   
class cieQ(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    no=models.IntegerField(default=0)
    clo1=models.FileField(upload_to='',null=True)
    clo2=models.FileField(upload_to='',null=True)
    clo3=models.FileField(upload_to='',null=True)
    clo4=models.FileField(upload_to='',null=True)
    clo5=models.FileField(upload_to='',null=True)
    clo6=models.FileField(upload_to='',null=True)
    def __str__(self):
        return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode)+" - "+str(self.student.studentId))
class cieQA(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    no=models.IntegerField(default=0)
    ques=models.FileField(upload_to='',null=True)
    duration=models.IntegerField(default=0)
    start=models.DateTimeField(null=True,blank=True)
    on=models.IntegerField(default=0)
    def __str__(self):
        return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode))
class semQA(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    ques=models.FileField(upload_to='',null=True)
    duration=models.IntegerField(default=0)
    start=models.DateTimeField(null=True,blank=True)
    on=models.IntegerField(default=0)
    def __str__(self):
        return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode))
class semQ(models.Model):
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    clo1=models.FileField(upload_to='',null=True)
    clo2=models.FileField(upload_to='',null=True)
    clo3=models.FileField(upload_to='',null=True)
    clo4=models.FileField(upload_to='',null=True)
    clo5=models.FileField(upload_to='',null=True)
    def __str__(self):
        return str(self.dept.name+" - "+str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.courseCode)+" - "+str(self.student.studentId))