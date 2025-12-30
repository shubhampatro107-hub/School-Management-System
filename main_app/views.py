from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt

from .EmailBackend import EmailBackend
from .models import Attendance, Session, Subject


# ================= LOGIN =================

def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("staff_home"))
        else:
            return redirect(reverse("student_home"))
    return render(request, 'main_app/login.html')


def doLogin(request):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")

    user = EmailBackend.authenticate(
        request,
        username=request.POST.get('email'),
        password=request.POST.get('password')
    )

    if user is not None:
        login(request, user)
        if user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif user.user_type == '2':
            return redirect(reverse("staff_home"))
        else:
            return redirect(reverse("student_home"))
    else:
        messages.error(request, "Invalid email or password")
        return redirect("/")


def logout_user(request):
    logout(request)
    return redirect("/")


# ================= AJAX ATTENDANCE =================

@csrf_exempt
def get_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')

    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = Attendance.objects.filter(subject=subject, session=session)

        attendance_list = []
        for attd in attendance:
            attendance_list.append({
                "id": attd.id,
                "attendance_date": str(attd.date),
                "session": attd.session.id
            })

        return JsonResponse(attendance_list, safe=False)

    except Exception:
        return JsonResponse([], safe=False)


# ================= FIREBASE =================

def showFirebaseJS(request):
    data = """
    importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-app.js');
    importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-messaging.js');

    firebase.initializeApp({
        apiKey: "AIzaSyBarDWWHTfTMSrtc5Lj3Cdw5dEvjAkFwtM",
        authDomain: "sms-with-django.firebaseapp.com",
        databaseURL: "https://sms-with-django.firebaseio.com",
        projectId: "sms-with-django",
        storageBucket: "sms-with-django.appspot.com",
        messagingSenderId: "945324593139",
        appId: "1:945324593139:web:03fa99a8854bbd38420c86"
    });

    const messaging = firebase.messaging();
    messaging.setBackgroundMessageHandler(function (payload) {
        const notification = payload.notification;
        return self.registration.showNotification(
            notification.title,
            {
                body: notification.body,
                icon: notification.icon
            }
        );
    });
    """
    return HttpResponse(data, content_type='application/javascript')
