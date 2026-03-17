from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class security_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    gender=models.CharField(max_length=100)
    photo=models.FileField()


class User_table(models.Model):
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=100)
    photo = models.FileField()


class complaint_table(models.Model):
    USER=models.ForeignKey(User_table,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)
    date=models.DateField()
    status=models.CharField(max_length=100)


class visitor_table(models.Model):
    name=models.CharField(max_length=100)
    USER=models.ForeignKey(User_table,on_delete=models.CASCADE)
    phone=models.BigIntegerField()
    photo=models.FileField()
    date = models.DateField()
    timeIN=models.TimeField()
    timeOUT=models.TimeField()


class notification_table(models.Model):
    message=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()


class chat_table(models.Model):
    From = models.ForeignKey(User,on_delete=models.CASCADE,related_name='fromid')
    To = models.ForeignKey(User,on_delete=models.CASCADE,related_name='toid')
    message = models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()


class emergency_notification_table(models.Model):
    USER=models.ForeignKey(User_table, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()


class camera_table(models.Model):
    camera_no=models.BigIntegerField()
    location=models.CharField(max_length=100)
    date= models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=100)

class QR_code_table(models.Model):
    timeIN = models.TimeField()
    timeOUT = models.TimeField()
    date = models.DateField()


class schedule_table(models.Model):
    USER = models.ForeignKey(User_table, on_delete=models.CASCADE)
    timeIN = models.TimeField()
    timeOUT = models.TimeField()


class alert_table(models.Model):
    alert = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()



class RaggingEvidence(models.Model):
    CAMERA=models.ForeignKey(camera_table,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=10)
    video = models.FileField(upload_to="videos/")
    audio = models.FileField(upload_to="audio/")
    verified = models.BooleanField(default=False)
    date = models.DateField()



class RaggingInvolvedStudent(models.Model):
    STUDENT = models.ForeignKey(User_table, on_delete=models.CASCADE)
    EVIDENCE = models.ForeignKey(RaggingEvidence, on_delete=models.CASCADE)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('STUDENT', 'EVIDENCE')




class Dangerous_person(models.Model):
    date=models.DateField()
    name=models.CharField(max_length=100)
    photo=models.FileField()
    details=models.CharField(max_length=500)
    SECURITY = models.ForeignKey(security_table, on_delete=models.CASCADE)




class unknown_person_table(models.Model):
     photo = models.FileField()
     camera_no = models.ForeignKey(camera_table, on_delete=models.CASCADE)
     dangerous = models.ForeignKey(Dangerous_person, on_delete=models.CASCADE, null=True, blank=True)
     date = models.DateField()
     time = models.TimeField()
     type=models.CharField(max_length=100)



class suspicious_activities(models.Model):
    CAMERA=models.ForeignKey(camera_table,on_delete=models.CASCADE)
    image=models.FileField()
    date=models.DateField()
    status=models.CharField(max_length=100,default='notification')



class danger_notification(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=100, default='pending')
    message = models.CharField(max_length=100)
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    DANGER=models.ForeignKey(unknown_person_table,on_delete=models.CASCADE)


class emergency_notification_status(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=100, default='pending')
    message = models.CharField(max_length=100)
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    EMERGENCY=models.ForeignKey(emergency_notification_table,on_delete=models.CASCADE)



class ragging_notification_status(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=100, default='pending')
    message = models.CharField(max_length=100)
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    RAGGING=models.ForeignKey(RaggingEvidence,on_delete=models.CASCADE)



class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)