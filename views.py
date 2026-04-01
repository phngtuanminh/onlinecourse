from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission
import logging

logger = logging.getLogger(__name__)


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def index(request):
    course_list = Course.objects.order_by('-total_enrollment')[:10]
    context = {'course_list': course_list}
    if request.user.is_authenticated:
        enrolled_courses = request.user.enrollment_set.values_list('course_id', flat=True)
        for course in course_list:
            if course.id in enrolled_courses:
                course.is_enrolled = True
    return render(request, 'onlinecourse/course_list_bootstrap.html', context)


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    if user.is_authenticated:
        try:
            Enrollment.objects.get(user=user, course=course)
        except Enrollment.DoesNotExist:
            Enrollment.objects.create(user=user, course=course, mode='honor')
            course.total_enrollment += 1
            course.save()
    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


def course_details(request, course_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    context['course'] = course
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            context['enrollment'] = enrollment
        except Enrollment.DoesNotExist:
            pass
    return render(request, 'onlinecourse/course_detail_bootstrap.html', context)


def submit(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    if user.is_authenticated:
        enrollment = get_object_or_404(Enrollment, user=user, course=course)
        submission = Submission.objects.create(enrollment=enrollment)
        selected_ids = []
        for key, values in request.POST.items():
            if key.startswith('choice'):
                for value in request.POST.getlist(key):
                    selected_ids.append(int(value))
                    choice = get_object_or_404(Choice, pk=int(value))
                    submission.choices.add(choice)
        submission.save()
        return HttpResponseRedirect(
            reverse('onlinecourse:show_exam_result', args=(course_id, submission.id))
        )


def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = submission.choices.values_list('id', flat=True)

    total_score = 0
    questions = course.question_set.all()
    for question in questions:
        question_choice_ids = [
            choice.id for choice in question.choice_set.filter(id__in=selected_ids)
        ]
        if question.is_get_score(question_choice_ids):
            total_score += question.grade

    context['course'] = course
    context['submission'] = submission
    context['selected_ids'] = selected_ids
    context['total_score'] = total_score
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
