# onlinecourse
# Django Online Course App

A Django-based Online Course application with exam features including models, views, templates, and result evaluation.

## Features

- User registration and login
- Course listing and enrollment
- Lessons per course
- Exam with multiple-choice questions
- Automatic score evaluation
- Result review with correct answers highlighted

## Models

- **Instructor** – course instructors
- **Learner** – enrolled learners
- **Course** – course details
- **Lesson** – course lessons
- **Enrollment** – user-course enrollment
- **Question** – exam questions linked to courses
- **Choice** – answer choices for questions
- **Submission** – stores learner exam submissions

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then go to `http://127.0.0.1:8000/admin` to add courses, lessons, questions, and choices.

## Project Structure

```
onlinecourse/
├── manage.py
├── requirements.txt
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── onlinecourse/
    ├── models.py       ← Question, Choice, Submission models here
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── templates/
        └── onlinecourse/
            ├── base.html
            ├── course_list_bootstrap.html
            ├── course_detail_bootstrap.html
            ├── exam_result_bootstrap.html
            ├── user_login_bootstrap.html
            └── user_registration_bootstrap.html
```
