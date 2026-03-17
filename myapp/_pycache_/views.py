import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect



###ran main.py for violence detection
###run stranger detection for criminal detection

# Create your views here.
from ai_service.face_recognition_service import recognize_students_from_video

from FlatSecurity import settings
from myapp.models import *
from django.contrib.auth.models import User,Group


def main(request):
    return render(request,"login.html")

def logout(request):
    return render(request,"login.html")


def login_get(request):
    if request.method=="POST":
        username=request.POST["Username"]
        password = request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.groups.filter(name="Admin").exists():
                login(request,user)
                return redirect('/myapp/home/')
            elif user.groups.filter(name="Expert").exists():
                login(request,user)
                return redirect('/myapp/viewusers/')
        else:
            return redirect('/myapp/main/')
        return redirect('/myapp/main/')

@login_required(login_url='/myapp/main/')
def home(request):
    return render(request,"home.html")


from django.shortcuts import render, redirect
from .models import camera_table
from datetime import datetime


def add_camera_POST(request):
    if request.method == "POST":
        c_no = request.POST.get('camera_no')
        loc = request.POST.get('location')

        # Automatic fields
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        obj = camera_table()
        obj.camera_no = c_no
        obj.location = loc
        obj.date = current_date
        obj.time = current_time
        obj.status = "Active"  # Default status
        obj.save()

        return redirect('/myapp/view_camera/')
    else:
        return render(request,'Admin/add_camers.html')


@login_required(login_url='/myapp/main/')
def add_notification(request):
    return render(request, "Admin/add_notification.html")

@login_required(login_url='/myapp/main/')
def add_notification_POST(request):
    notification=request.POST['notification']
    ob=notification_table()
    ob.message=notification
    ob.date=datetime.now()
    ob.time=datetime.now()
    ob.save()
    return redirect('/myapp/view_notification/')


@login_required(login_url='/myapp/main/')
def add_staff(request):
    return render(request, "Admin/add_staff.html")


@login_required(login_url='/myapp/main/')
def add_staff_POST(request):
    Name=request.POST['name']
    email=request.POST['email']
    Phone_Number=request.POST['phone']
    gender=request.POST['gender']
    username=request.POST['username']
    password=request.POST['password']
    photo=request.FILES['photo']

    user = User.objects.create(
        username=username,
        password=make_password(password),
        email=email,
        first_name=request.POST.get('name')
    )
    user.groups.add(Group.objects.get(name='Security'))
    user.save()

    ob=security_table()
    ob.name=Name
    ob.email=email
    ob.phone=Phone_Number
    ob.gender=gender
    ob.photo=photo
    ob.LOGIN=user
    ob.save()
    return redirect('/myapp/view_staff/')


@login_required(login_url='/myapp/main/')
def edit_staff(request,id):
    request.session['id']=id
    a=security_table.objects.get(id=id)
    return render(request, "Admin/edit_staff.html",{'data':a})


@login_required(login_url='/myapp/main/')
def edit_staff_POST(request):
    name = request.POST['name']
    email = request.POST['email']
    phone_number = request.POST['phone_number']
    gender = request.POST['gender']


    ob = security_table.objects.get(id=request.session['id'])

    if 'photo' in request.FILES:
        photo=request.FILES['photo']
        ob.photo=photo
        ob.save()

    ob.name = name
    ob.email = email
    ob.phone = phone_number
    ob.gender = gender

    ob.save()
    return redirect('/myapp/view_staff/')


@login_required(login_url='/myapp/main/')
def send_replay(request,id):
    request.session['sid']=id
    return render(request, "Admin/send_replay.html")


@login_required(login_url='/myapp/main/')
def send_replay_POST(request):
    reply=request.POST['reply']

    ob=complaint_table.objects.get(id=request.session['sid'])
    ob.reply=reply
    ob.save()
    return redirect('/myapp/view_complaint/')


@login_required(login_url='/myapp/main/')
def view_complaint(request):
    a = complaint_table.objects.all()
    return render(request, "Admin/view_complaint.html",{'data':a})

@login_required(login_url='/myapp/main/')
def view_notification(request):
    a = notification_table.objects.all()
    return render(request, "Admin/view_notification.html",{'data':a})

@login_required(login_url='/myapp/main/')
def view_camera(request):
    a = camera_table.objects.all()
    return render(request, "Admin/view camera.html",{'data':a})


def delete_camera(request,id):
    camera_table.objects.get(id=id).delete()
    return redirect('/myapp/view_camera/')

def view_staff(request):
    a=security_table.objects.all()
    return render(request, "Admin/view_staff.html",{'data':a})


@login_required(login_url='/myapp/main/')
def view_visitor(request):
    a=visitor_table.objects.all()
    return render(request, "Admin/view_visitor.html",{'data':a})


@login_required(login_url='/myapp/main/')
def edit_notification(request,id):
    request.session['id']=id
    b=notification_table.objects.get(id=id)
    return render(request, "Admin/edit_notification.html",{'data':b})


@login_required(login_url='/myapp/main/')
def edit_notification_POST(request):
    notification = request.POST['notification']

    ob = notification_table.objects.get(id=request.session['id'])
    ob.message = notification
    ob.date = datetime.now()
    ob.time = datetime.now()
    ob.save()
    return redirect('/myapp/view_notification/')

@login_required(login_url='/myapp/main/')
def delete_staff(request,id):
    ob=security_table.objects.get(id=id)
    ob.delete()
    return redirect('/myapp/view_staff/')


@login_required(login_url='/myapp/main/')
def delete_notification(request,id):
    ob=notification_table.objects.get(id=id)
    ob.delete()
    return redirect('/myapp/view_notification/')


##################flutter#################

def loginpost(request):
    username = request.POST['username']
    print(username)
    password = request.POST['password']
    print(password)

    u = authenticate(request, username=username, password=password)
    print(u)

    if u is not None:
        if u.groups.filter(name='User').exists():
            print('user login success')
            login(request,u)
            return JsonResponse({"status": "ok",'lid':request.user.id,'type':'User'})
        elif u.groups.filter(name='Security').exists():
            print('security login success')
            login(request,u)
            return JsonResponse({"status": "ok",'lid':request.user.id,'type':'Security'})
        else:
            return  JsonResponse({"status": "no"})
    print('error')
    return  JsonResponse({"status":"no"})



def user_registration(request):
    username = request.POST['username']
    password = request.POST['password']
    name=request.POST['name']
    gender=request.POST['gender']
    place=request.POST['place']
    post=request.POST['post']
    district=request.POST['district']
    phone=request.POST['phone']
    email=request.POST['email']
    photo=request.FILES['photo']

    user = User.objects.create(
        username=username,
        password=make_password(password),
        email=email,
        first_name=password
    )
    user.save()
    user.groups.add(Group.objects.get(name="User"))
    ob = User_table()
    ob.LOGIN = user
    ob.name = name
    ob.gender=gender
    ob.place=place
    ob.post=post
    ob.district=district
    ob.phone=phone
    ob.email=email
    ob.photo=photo
    ob.save()

    return JsonResponse({'status':'ok'})

def send_complaint(request):
    lid=request.POST['lid']
    complaint=request.POST['complaint']

    ob=complaint_table()
    ob.complaint=complaint
    ob.reply='pending'
    ob.date=datetime.now()
    ob.status='pending'
    ob.USER=User_table.objects.get(LOGIN__id=lid)
    ob.save()
    return JsonResponse({'status':'ok'})


def user_view_reply(request):
    lid=request.POST['lid']
    c=complaint_table.objects.filter(USER__LOGIN_id=lid)
    l=[]
    for i in c:
        l.append({
            'id':i.id,
            'date':i.date,
            'complaint':i.complaint,
            'reply':i.reply,
            'status':i.status,


        })
    return JsonResponse({'status':'ok','data':l})


def user_add_visitor_schedule(request):
    lid = request.POST['lid']
    name = request.POST['name']
    phone = request.POST['phone']
    photo = request.FILES['photo']
    date = request.POST['date']
    timeIN = request.POST['timeIN']
    timeOUT = request.POST['timeOUT']

    ob = visitor_table()
    ob.name = name
    ob.phone = phone
    ob.photo = photo
    ob.date = date
    ob.timeIN = timeIN
    ob.timeOUT = timeOUT
    ob.USER = User_table.objects.get(LOGIN__id=lid)
    ob.save()

    return JsonResponse({'status': 'ok', 'vid': ob.id})



def user_View_visitor_schedule(request):
    lid = request.POST['lid']
    c = visitor_table.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in c:
        l.append({
            'id': str(i.id),
            'name': i.name,
            'photo':request.build_absolute_uri(i.photo.url),
            'date': i.date,
            'phone': str(i.phone),
            'timeIN': i.timeIN,
            'timeOUT': i.timeOUT,

        })
    return JsonResponse({'status': 'ok','data':l})

def user_delete_visitor_schedule(request):
    id=request.POST['vid']
    ob=visitor_table.objects.get(id=id)
    ob.delete()
    return JsonResponse({'status': 'ok'})

def user_view_notification(request):
    c = notification_table.objects.all()
    l = []
    for i in c:
        l.append({
            'message': i.message,
            'date': i.date,
            'time': i.time,

        })
    return JsonResponse({'status': 'ok','data':l})


def user_view_security(request):
    c = security_table.objects.all()
    l = []
    for i in c:
        photo=request.build_absolute_uri(i.photo.url)if i.photo else""
        l.append({
            'id': i.id,
            'name': i.name,
            'email': i.email,
            'phone': i.phone,
            'gender': i.gender,
            'photo': photo,
            'login': i.LOGIN.id,

        })
    return JsonResponse({'status': 'ok','data':l})




def security_user_user(request):
    c = User_table.objects.all()
    l = []
    for i in c:
        photo=request.build_absolute_uri(i.photo.url)if i.photo else""
        l.append({
            'id': str(i.id),
            'name': i.name,
            'place': i.place,
            'post': i.post,
            'district': i.district,
            'email': i.email,
            'phone': str(i.phone),
            'gender': i.gender,
            'photo': photo,
            'login': str(i.LOGIN.id),

        })
    return JsonResponse({'status': 'ok','data':l})




from django.utils import timezone
from django.http import JsonResponse

def User_sendchat(request):
    FROM_id = request.POST['from_id']
    TOID_id = request.POST['to_id']
    msg = request.POST['message']

    c = chat_table()
    c.From_id = FROM_id
    c.To_id = TOID_id
    c.message = msg
    c.time=datetime.now().strftime('%H:%M')
    c.date = timezone.now()  # ✅ timezone-aware UTC
    c.save()
    return JsonResponse({'status': "ok"})


def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    from django.db.models import Q

    res = chat_table.objects.filter(Q(From_id=fromid, To_id=toid) | Q(From_id=toid, To_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id,
                  "msg": i.message,
                  "from": i.From_id,
                  "date": i.date,
                  "time": i.time,
                  "to": i.To_id})

    return JsonResponse({"status":"ok",'data':l})





def user_add_emergency_notification(request):
    lid = request.POST['lid']
    message = request.POST['message']
    date = datetime.now().date()
    time = datetime.now().time()

    ob = emergency_notification_table()
    ob.message = message
    ob.date = date
    ob.time = time
    ob.USER = User_table.objects.get(LOGIN__id=lid)
    ob.save()
    return JsonResponse({'status': 'ok'})

def user_view_emergency_notification(request):
    lid = request.POST['lid']
    c = emergency_notification_table.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in c:
        l.append({
            'id': i.id,
            'message': i.message,
            'date': i.date,
            'time': i.time,

        })
    return JsonResponse({'status': 'ok','data':l})




def user_delete_emergency_notification(request):
    id = request.POST['vid']
    ob = emergency_notification_table.objects.get(id=id)
    ob.delete()
    return JsonResponse({'status': 'ok'})




def user_view_notification_other(request):
    lid=request.POST['lid']
    c = emergency_notification_table.objects.exclude(USER__LOGIN_id=lid)
    l = []
    for i in c:
        l.append({
            'id': i.id,
            'message': i.message,
            'date': i.date,
            'time': i.time,
            'username': i.USER.name,
            'phone': i.USER.phone,

        })
    return JsonResponse({'status': 'ok','data':l})


##################

def security_scan_validate_QR_entry_exit(request):
    return JsonResponse({'status': 'ok'})

def security_view_notification(request):
    c = emergency_notification_table.objects.all()
    l = []
    for i in c:
        l.append({
            'id': i.id,
            'message': i.message,
            'date': i.date,
            'time': i.time,
            'username': i.USER.name,
            'phone':i.USER.phone,

        })
    return JsonResponse({'status': 'ok','data':l})

def security_respond_emergency_alert(request):
    return JsonResponse({'status': 'ok'})

def security_unknown_person(request):
    c = unknown_person_table.objects.all()
    l = []
    for i in c:
        l.append({
            'photo': i.photo,
            'camera_no': i.camera_no,
            'date': i.date,
            'time': i.time,

        })
    return JsonResponse({'status': 'ok','data':l})


def user_view_profile(request):
    lid=request.POST['lid']
    print(lid,'lllllllllll')
    ob=User_table.objects.get(LOGIN=lid)
    return JsonResponse({'status': 'ok',
                         'name': str(ob.name),
                         'gender': str(ob.gender),
                         'place': str(ob.place),
                         'post': str(ob.post),
                         'district': str(ob.district),
                         'phone': str(ob.phone),
                         'email': str(ob.email),
                         'photo': request.build_absolute_uri(ob.photo.url)if ob.photo else""
                         })


def edit_profile(request):
    name=request.POST['name']
    gender=request.POST['gender']
    place=request.POST['place']
    post=request.POST['post']
    district=request.POST['district']
    phone=request.POST['phone']
    email=request.POST['email']
    lid=request.POST['lid']
    ob = User_table.objects.get(LOGIN=lid)
    if 'photo' in request.FILES:

        photo=request.FILES['photo']
        ob.photo = photo
        ob.save()

    ob.name = name
    ob.gender=gender
    ob.place=place
    ob.post=post
    ob.district=district
    ob.phone=phone
    ob.email=email
    ob.save()

    return JsonResponse({'status':'ok'})




from datetime import datetime
from django.http import JsonResponse
from myapp.models import *
from django.utils import timezone


# ─────────────────────────────────────────────────────────────────────────────
# SECURITY: Scan & Validate QR Code
# POST params: vid (visitor_table id), security_id (security_table LOGIN id)
#
# Logic:
#   1. Find the visitor record by id
#   2. Check today's date matches visitor's scheduled date
#   3. Check current time is within timeIN and timeOUT
#   4. If valid → return visitor info + "ALLOW"
#   5. If invalid → return reason + "DENY"
# ─────────────────────────────────────────────────────────────────────────────
from datetime import datetime
from django.http import JsonResponse
from myapp.models import *


def security_scan_validate_QR(request):
    try:
        vid = request.POST.get('vid')
        if not vid:
            return JsonResponse({'status': 'error', 'message': 'No QR data received'})

        try:
            visitor = visitor_table.objects.get(id=vid)
        except visitor_table.DoesNotExist:
            return JsonResponse({
                'status': 'deny',
                'reason': 'Invalid QR Code — visitor not found',
                'allow': False
            })

        # Use plain datetime.now() — naive, matches naive DB time fields
        now = datetime.now()
        today = now.date()
        # Strip microseconds so comparison is clean
        current_time = now.time().replace(microsecond=0)

        # Debug print — check your server logs to confirm times
        print(f"DEBUG → current_time: {current_time}  |  timeIN: {visitor.timeIN}  |  timeOUT: {visitor.timeOUT}  |  today: {today}  |  visit_date: {visitor.date}")

        # Check date
        if visitor.date != today:
            return JsonResponse({
                'status': 'deny',
                'reason': f'Wrong date. Pass valid on {visitor.date}, today is {today}',
                'allow': False,
                'visitor_name': visitor.name,
                'scheduled_date': str(visitor.date),
                'photo': request.build_absolute_uri(visitor.photo.url) if visitor.photo else '',
            })

        # Normalize DB time fields — strip microseconds for safe comparison
        time_in  = visitor.timeIN.replace(microsecond=0)
        time_out = visitor.timeOUT.replace(microsecond=0)

        # Check time window
        if not (time_in <= current_time <= time_out):
            return JsonResponse({
                'status': 'deny',
                'reason': (
                    f'Outside allowed time window.\n'
                    f'Allowed: {time_in.strftime("%H:%M")} – {time_out.strftime("%H:%M")}\n'
                    f'Current time: {current_time.strftime("%H:%M")}'
                ),
                'allow': False,
                'visitor_name': visitor.name,
                'scheduled_date': str(visitor.date),
                'time_in': time_in.strftime('%H:%M'),
                'time_out': time_out.strftime('%H:%M'),
                'current_time': current_time.strftime('%H:%M'),
                'photo': request.build_absolute_uri(visitor.photo.url) if visitor.photo else '',
            })

        # All checks passed → ALLOW
        log = QR_code_table()
        log.date   = today
        log.timeIN  = visitor.timeIN
        log.timeOUT = visitor.timeOUT
        log.save()

        return JsonResponse({
            'status': 'allow',
            'allow': True,
            'visitor_name': visitor.name,
            'visitor_phone': str(visitor.phone),
            'scheduled_date': str(visitor.date),
            'time_in': time_in.strftime('%H:%M'),
            'time_out': time_out.strftime('%H:%M'),
            'flat_owner': visitor.USER.name,
            'flat_owner_phone': str(visitor.USER.phone),
            'photo': request.build_absolute_uri(visitor.photo.url) if visitor.photo else '',
        })

    except Exception as e:
        print(f"QR Scan Error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e), 'allow': False})
# ─────────────────────────────────────────────────────────────────────────────
# SECURITY: View all scheduled visitors for today
# ─────────────────────────────────────────────────────────────────────────────
def security_view_today_visitors(request):
    today = datetime.now().date()
    visitors = visitor_table.objects.filter(date=today)
    l = []
    for v in visitors:
        l.append({
            'id': v.id,
            'name': v.name,
            'phone': str(v.phone),
            'photo': request.build_absolute_uri(v.photo.url) if v.photo else '',
            'date': str(v.date),
            'timeIN': v.timeIN.strftime('%H:%M'),
            'timeOUT': v.timeOUT.strftime('%H:%M'),
            'flat_owner': v.USER.name,
            'flat_owner_phone': str(v.USER.phone),
        })
        print(l,'lllllll')
    return JsonResponse({'status': 'ok', 'data': l})


# ─────────────────────────────────────────────────────────────────────────────
# SECURITY: View all emergency notifications from users
# ─────────────────────────────────────────────────────────────────────────────
def security_view_emergency(request):
    alerts = emergency_notification_table.objects.all().order_by('-id')
    l = []
    for a in alerts:
        l.append({
            'id': a.id,
            'message': a.message,
            'date': str(a.date),
            'time': str(a.time),
            'username': a.USER.name,
            'phone': str(a.USER.phone),
            'flat': a.USER.place,
        })
    return JsonResponse({'status': 'ok', 'data': l})


# ─────────────────────────────────────────────────────────────────────────────
# SECURITY: View security profile
# POST params: lid (security LOGIN user id)
# ─────────────────────────────────────────────────────────────────────────────
def security_view_profile(request):
    lid = request.POST.get('lid')
    try:
        sec = security_table.objects.get(LOGIN__id=lid)
        return JsonResponse({
            'status': 'ok',
            'name': sec.name,
            'email': sec.email,
            'phone': str(sec.phone),
            'gender': sec.gender,
            'photo': request.build_absolute_uri(sec.photo.url) if sec.photo else '',
        })
    except security_table.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Profile not found'})


# ─────────────────────────────────────────────────────────────────────────────
# SECURITY: View all visitors (history — all dates)
# ─────────────────────────────────────────────────────────────────────────────
def security_view_all_visitors(request):
    visitors = visitor_table.objects.all().order_by('-date')
    l = []
    for v in visitors:
        l.append({
            'id': v.id,
            'name': v.name,
            'phone': str(v.phone),
            'photo': request.build_absolute_uri(v.photo.url) if v.photo else '',
            'date': str(v.date),
            'timeIN': v.timeIN.strftime('%H:%M'),
            'timeOUT': v.timeOUT.strftime('%H:%M'),
            'flat_owner': v.USER.name,
        })
    return JsonResponse({'status': 'ok', 'data': l})





def user_view_dangerous_person(request):
    visitors = Dangerous_person.objects.all()
    l = []
    for v in visitors:
        l.append({
            'id': v.id,
            'name': v.name,
            'details': v.details,
            'photo': request.build_absolute_uri(v.photo.url) if v.photo else '',
            'date': str(v.date),

        })
    return JsonResponse({'status': 'ok', 'data': l})


#############


def security_view_dangerous_person(request):
    lid=request.POST['lid']
    visitors = Dangerous_person.objects.filter(SECURITY__LOGIN_id=lid)
    l = []
    for v in visitors:
        l.append({
            'id': v.id,
            'name': v.name,
            'details': v.details,
            'photo': request.build_absolute_uri(v.photo.url) if v.photo else '',
            'date': str(v.date),

        })
    return JsonResponse({'status': 'ok', 'data': l})


def security_view_camera_notification(request):
    visitors = unknown_person_table.objects.all()
    l = []
    for v in visitors:

        if v.type == 'Dangerous Person':

            l.append({
                'id': v.id,
                'name': v.dangerous.name,
                'camera_no': v.camera_no.camera_no,
                'photo': request.build_absolute_uri(v.photo.url) if v.photo else '',
                'date': str(v.date),
                'time': str(v.time),
                'type': str(v.type),

            })

        elif v.type == 'Unknown Person':
            l.append({
                'id': v.id,
                'name': "Unknown Person",
                'camera_no': v.camera_no.camera_no,
                'photo': request.build_absolute_uri(v.photo.url) if v.photo else '',
                'date': str(v.date),
                'time': str(v.time),
                'type': str(v.type),

            })



    return JsonResponse({'status': 'ok', 'data': l})


def add_dangerous_person(request):
    lid=request.POST['lid']
    name=request.POST['name']
    details=request.POST['details']
    photo=request.FILES['photo']
    obj=Dangerous_person()
    obj.date=datetime.now().today()
    obj.name=name
    obj.photo=photo
    obj.details=details
    obj.SECURITY=security_table.objects.get(LOGIN=lid)
    obj.save()
    return JsonResponse({'status':'ok'})


def delete_dangerous_person(request):
    id=request.POST['id']
    Dangerous_person.objects.get(id=id).delete()
    return JsonResponse({'status':'ok'})





def security_view_violence_detection(request):
    visitors = RaggingEvidence.objects.all()
    l = []
    for v in visitors:
        l.append({
            'id': str(v.id),
            'camera': str(v.CAMERA.camera_no),
            'location': v.CAMERA.location,
            'timestamp': v.timestamp,
            'severity': v.severity,
            'video': request.build_absolute_uri(v.video.url) if v.video else '',
            'audio': request.build_absolute_uri(v.audio.url) if v.audio else '',
            'date': str(v.date),

        })
    return JsonResponse({'status': 'ok', 'data': l})


# "======================================================main============================================="


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import threading

def ragging_alert_api(request):
    if request.method == "POST":
        severity = request.POST.get("severity")
        video = request.FILES.get("video")
        audio = request.FILES.get("audio")

        if not severity or not video:
            return JsonResponse({"status": "error"}, status=400)

        evidence = RaggingEvidence.objects.create(
            severity=severity,
            video=video,
            CAMERA=camera_table.objects.get(id=1),
            audio=audio,
            verified='True',
            timestamp=datetime.now(),
            date=datetime.now().today()
        )

        # 🔥 start thread AFTER evidence saved
        t = threading.Thread(
            target=recognize_students_from_video,
            args=(evidence.id,),
            daemon=True
        )
        t.start()

        return JsonResponse({
            "status": "ok",
            "evidence_id": evidence.id
        })

    return JsonResponse({"status": "error"}, status=405)



def detect_noti(request):
    img=request.FILES['image']
    cam_id=request.POST['cam_id']
    ob=suspicious_activities()
    ob.CAMERA=camera_table.objects.get(id=cam_id)
    ob.image=img
    ob.date=datetime.today()
    ob.save()
    return  JsonResponse({"task":"ok"})




#####################################33dang



# import cv2
# import os
# import numpy as np
# from django.http import JsonResponse
# from django.core.files.base import ContentFile
# from datetime import datetime
# from deepface import DeepFace
# from .models import Dangerous_person, unknown_person_table
#
#
# def check_stranger_api(request):
#
#     if request.method == "POST" and request.FILES.get("image"):
#
#         img_file = request.FILES["image"]
#
#         # Convert uploaded image to OpenCV frame
#         nparr = np.frombuffer(img_file.read(), np.uint8)
#         frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
#         students = Dangerous_person.objects.all()
#
#         is_identified = False
#
#         for student in students:
#
#             student_photo_path = student.photo.path
#
#             if not os.path.exists(student_photo_path):
#                 continue
#
#             try:
#
#                 result = DeepFace.verify(
#                     img1_path=frame,
#                     img2_path=student_photo_path,
#                     model_name="VGG-Face",   # more stable
#                     detector_backend="opencv",
#                     enforce_detection=False
#                 )
#
#                 print("Verification result:", result)
#
#                 # relaxed threshold
#                 if result["verified"] or result["distance"] < 0.55:
#
#                     is_identified = True
#
#                     _, buffer = cv2.imencode('.jpg', frame)
#
#                     content = ContentFile(
#                         buffer.tobytes(),
#                         name=f"dangerous_{os.urandom(4).hex()}.jpg"
#                     )
#
#                     camera_no = 1
#
#                     intruder = unknown_person_table.objects.create(
#                         photo=content,
#                         camera_no_id=camera_no,
#                         dangerous_id=student.id,
#                         date=datetime.now().date(),
#                         time=datetime.now().time(),
#                         type="Dangerous Person"
#                     )
#
#                     return JsonResponse({
#                         "status": "dangerous",
#                         "name": student.name
#                     })
#
#             except Exception as e:
#                 print(f"Error verifying {student.name}: {e}")
#                 continue
#
#
#         # If no match found
#         if not is_identified:
#
#             _, buffer = cv2.imencode('.jpg', frame)
#
#             content = ContentFile(
#                 buffer.tobytes(),
#                 name=f"unknown_{os.urandom(4).hex()}.jpg"
#             )
#
#             camera_no = 1
#
#             intruder = unknown_person_table.objects.create(
#                 photo=content,
#                 camera_no_id=camera_no,
#                 dangerous=None,
#                 date=datetime.now().date(),
#                 time=datetime.now().time(),
#                 type="Unknown Person"
#             )
#
#             return JsonResponse({
#                 "status": "unknown",
#                 "message": "Unknown person logged",
#                 "id": intruder.id
#             })
#
#     return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

import cv2
import os
import numpy as np
from django.http import JsonResponse
from django.core.files.base import ContentFile
from datetime import datetime
from deepface import DeepFace
from .models import Dangerous_person, unknown_person_table, camera_table


def check_stranger_api(request):
    if request.method == "POST" and request.FILES.get("image"):
        img_file = request.FILES["image"]

        # Convert uploaded image to OpenCV frame
        nparr = np.frombuffer(img_file.read(), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # FIX: Ensure a camera exists to satisfy the Foreign Key constraint
        # In a real app, you might pass the camera_id in the request.POST
        camera_obj = camera_table.objects.first()
        if not camera_obj:
            return JsonResponse({
                "status": "error",
                "message": "No camera found in database. Please add a camera in admin."
            }, status=400)

        students = Dangerous_person.objects.all()
        is_identified = False

        for student in students:
            if not student.photo:
                continue

            student_photo_path = student.photo.path
            if not os.path.exists(student_photo_path):
                continue

            try:
                result = DeepFace.verify(
                    img1_path=frame,
                    img2_path=student_photo_path,
                    model_name="VGG-Face",
                    detector_backend="opencv",
                    enforce_detection=False
                )

                # Relaxed threshold logic
                if result["verified"] or result["distance"] < 0.55:
                    is_identified = True
                    _, buffer = cv2.imencode('.jpg', frame)
                    content = ContentFile(
                        buffer.tobytes(),
                        name=f"dangerous_{os.urandom(4).hex()}.jpg"
                    )

                    # Create record for Dangerous Person
                    intruder = unknown_person_table.objects.create(
                        photo=content,
                        camera_no=camera_obj,  # Pass the actual object, not an ID
                        dangerous=student,  # Pass the student object
                        date=datetime.now().date(),
                        time=datetime.now().time(),
                        type="Dangerous Person"
                    )

                    return JsonResponse({
                        "status": "dangerous",
                        "name": student.name
                    })

            except Exception as e:
                print(f"Error verifying {student.name}: {e}")
                continue

        # If no match found, log as Unknown
        if not is_identified:
            _, buffer = cv2.imencode('.jpg', frame)
            content = ContentFile(
                buffer.tobytes(),
                name=f"unknown_{os.urandom(4).hex()}.jpg"
            )

            intruder = unknown_person_table.objects.create(
                photo=content,
                camera_no=camera_obj,
                dangerous=None,
                date=datetime.now().date(),
                time=datetime.now().time(),
                type="Unknown Person"
            )

            return JsonResponse({
                "status": "unknown",
                "message": "Unknown person logged",
                "id": intruder.id
            })

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


##################################################################################################



def forgotpasswordflutter(request):
    email = request.POST['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})

    otp = random.randint(100000, 999999)
    PasswordResetOTP.objects.create(email=email, otp=otp)

    send_mail('Your Verification Code',
              f'Your verification code is {otp}',
              settings.EMAIL_HOST_USER,
              [email],
              fail_silently=False)
    return JsonResponse({'status': 'ok', 'message': 'OTP sent'})


def verifyOtpflutterPost(request):
    email = request.POST['email']
    entered_otp = request.POST['entered_otp']
    otp_obj = PasswordResetOTP.objects.filter(email=email).latest('created_at')
    if otp_obj.otp == entered_otp:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'})


def changePasswordflutter(request):
    email = request.POST['email']
    newpassword = request.POST['newPassword']
    confirmPassword = request.POST['confirmPassword']
    if newpassword == confirmPassword:
        try:
            user = User.objects.get(email=email)
            user.set_password(confirmPassword)
            user.save()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})


###



def forgot(request):
    return render(request,'forgot.html')

def forgotPassword_otp(request):
    email=request.POST['email']
    try:
        user=User.objects.get(email=email)
    except User.DoesNotExist:
        messages.warning(request,'Email doesnt match')
        return redirect('/myapp/')
    otp=random.randint(100000,999999)
    request.session['otp']=str(otp)
    request.session['email'] = email

    send_mail('Your Verification Code',
    f'Your verification code is {otp}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False)
    messages.success(request,'OTP sent To your Mail')
    return redirect('/myapp/verifyOtp/')

def verifyOtp(request):
    return render(request,'otpverification.html')

def verifyOtpPost(request):
    entered_otp=request.POST['entered_otp']
    if request.session.get('otp') == entered_otp:
        messages.success(request,'otp verified')
        return redirect('/myapp/new_password/')
    else:
        messages.warning(request,'Invalid OTP!!')
        return redirect('/myapp/')

def new_password(request):
    return render(request,'new_password.html')

def changePassword(request):
    newpassword=request.POST['newPassword']
    confirmPassword=request.POST['confirmPassword']
    if newpassword == confirmPassword:
        email=request.session.get('email')
        user = User.objects.get(email=email)
        user.set_password(confirmPassword)
        user.save()
        messages.success(request, 'Password Updated Successfully')
        return redirect('/myapp/')
    else:
        messages.warning(request, 'The password doesnt match!!')
        return redirect('/myapp/new_password/')






###################################################################3
from django.http import JsonResponse
from datetime import date
from .models import *

def get_notifications_dangerous(request):

    today = date.today()
    lid = request.POST.get('lid')

    if not lid:
        return JsonResponse({"status": "error", "msg": "lid is required"})

    user = User.objects.get(id=int(lid))

    notified_ids = danger_notification.objects.filter(
        LOGIN=user,
        date=today
    ).values_list('DANGER_id', flat=True)

    notification = unknown_person_table.objects.filter(
        dangerous__isnull=False
    ).exclude(
        id__in=notified_ids
    ).order_by('-id').first()

    if notification:

        msg = f"Detected Dangerous Person: {notification.dangerous.name}"

        danger_notification.objects.create(
            LOGIN=user,
            DANGER=notification,
            date=today,
            status='viewed',
            message=msg
        )

        return JsonResponse({
            "status": "ok",
            "msg": msg
        })

    return JsonResponse({"status": "na"})

##

def get_notifications_violence(request):

    today = date.today()
    lid = request.POST.get('lid')

    if not lid:
        return JsonResponse({"status": "error", "msg": "Login id missing"})

    try:
        user = User.objects.get(id=lid)
    except User.DoesNotExist:
        return JsonResponse({"status": "error", "msg": "User not found"})

    # Already notified evidence IDs
    notified_ids = ragging_notification_status.objects.filter(
        LOGIN=user,
        date=today
    ).values_list('RAGGING_id', flat=True)

    # Get new violence detection
    notification = RaggingEvidence.objects.filter(
        date=today
    ).exclude(
        id__in=notified_ids
    ).order_by('-id').first()


    if notification:

        msg = f"Detected Violence Person at {notification.CAMERA.location}"

        ragging_notification_status.objects.create(
            LOGIN=user,
            RAGGING=notification,
            date=today,
            status='viewed',
            message=msg
        )

        return JsonResponse({
            "status": "ok",
            "msg": msg
        })

    return JsonResponse({"status": "na"})

####

def get_notifications_emergency(request):
    today = date.today()
    lid = request.POST.get('lid')

    if not lid:
        return JsonResponse({"status": "error", "msg": "Login id missing"})

    try:
        user = User.objects.get(id=lid)
    except User.DoesNotExist:
        return JsonResponse({"status": "error", "msg": "User not found"})

    # Already notified evidence IDs
    notified_ids = emergency_notification_status.objects.filter(
        LOGIN=user,
        date=today
    ).values_list('EMERGENCY_id', flat=True)

    # Get new violence detection
    notification = emergency_notification_table.objects.filter(
        date=today
    ).exclude(
        id__in=notified_ids
    ).order_by('-id').first()

    if notification:
        msg = f"Emergency at {notification.USER.name}-{notification.USER.phone}-{notification.message}"

        emergency_notification_status.objects.create(
            LOGIN=user,
            EMERGENCY=notification,
            date=today,
            status='viewed',
            message=msg
        )

        return JsonResponse({
            "status": "ok",
            "msg": msg
        })

    return JsonResponse({"status": "na"})