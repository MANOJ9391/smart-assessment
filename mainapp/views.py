import random
import json
from django.shortcuts import render, redirect
from .models import Question, Result, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'home.html')
# START TEST
def start_test(request):
    questions = list(Question.objects.all())
    random.shuffle(questions)
    questions = questions[:10]

    request.session['question_ids'] = [q.id for q in questions]

    return render(request, 'test.html', {'questions': questions})

from django.shortcuts import render, redirect
from .models import Question, Result

def submit_test(request):

    # ❌ Block GET request
    if request.method != 'POST':
        return redirect('start_test')

    question_ids = request.session.get('question_ids', [])
    questions = Question.objects.filter(id__in=question_ids)

    score = 0
    total = len(questions)

    chapter_stats = {}

    # 🔥 Calculate performance
    for q in questions:
        selected = request.POST.get(f"q{q.id}")
        chapter = q.chapter.name

        if chapter not in chapter_stats:
            chapter_stats[chapter] = {'correct': 0, 'total': 0}

        chapter_stats[chapter]['total'] += 1

        if selected and str(selected) == str(q.correct_option):
            score += 1
            chapter_stats[chapter]['correct'] += 1

    # 🔥 Recommendations
    recommendations = {}

    for chapter, data in chapter_stats.items():
        accuracy = data['correct'] / data['total']

        if accuracy < 0.5:

            if chapter == "powersupply&amplifiers":
                recommendations[chapter] = {
                    "videos": [
                        "https://youtu.be/c0hmLifC2mk?si=i0j16KCWRI07DJ9R",
                
                    ],
                    "papers": [
                        "https://ieeexplore.ieee.org/document/8468201",
                        
                    ]
                }

            elif chapter == "oscillators and op-amp's":
                recommendations[chapter] = {
                    "videos": [
                        "https://youtu.be/tlwoLvWfPhg?si=zdoqd7fjXfKYbvAz"
                    ],
                    "papers": [
                        "https://ieeexplore.ieee.org/document/9051234"
                    ]
                }

            elif chapter == "communication systems":
                recommendations[chapter] = {
                    "videos": [
                       "https://youtu.be/gbPYMxRv0FY?si=LrUoqAbHpWQkFZz7"
                    ],
                    "papers": [
                        "https://ieeexplore.ieee.org/document/7324567"
                    ]
                }

    # 🔥 SAVE RESULT (FIXED POSITION)
    if request.user.is_authenticated:
        Result.objects.create(
        user=request.user,
        score=score,
        total=total,
        chapter_stats=chapter_stats,
        recommendations=recommendations
    )

    # 🔥 FINAL RESPONSE
    return render(request, 'result.html', {
        'score': score,
        'total': total,
        'chapter_stats': chapter_stats,
        'recommendations': recommendations
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')



def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        # create user
        user = User.objects.create_user(username=username, password=password)

        # login automatically after signup
        login(request, user)

        return redirect('home')

    return render(request, 'signup.html')


@login_required
def dashboard(request):
    results = Result.objects.filter(user=request.user).order_by('-created_at')  # ascending for chart

    total_tests = results.count()

    avg_score = 0
    best_score = 0

    # 🔥 NEW: chart data
    chart_data = []
    labels = []

    if total_tests > 0:
        avg_score = sum([(r.score / r.total) * 100 for r in results]) / total_tests
        best_score = max([r.score for r in results])

        # 👉 generate chart data
        for r in results:
            percentage = (r.score / r.total) * 100
            chart_data.append(round(percentage, 2))
            labels.append(r.created_at.strftime("%b %d"))  # e.g. May 03

    return render(request, 'dashboard.html', {
        'results': results.order_by('-created_at'),  # latest first for table
        'total_tests': total_tests,
        'avg_score': round(avg_score, 1),
        'best_score': best_score,
        'chart_data': json.dumps(chart_data),
        'labels': json.dumps(labels)
    })


@login_required
def view_result(request, id):
    result = get_object_or_404(Result, id=id, user=request.user)

    return render(request, 'result.html', {
        'score': result.score,
        'total': result.total,
        'chapter_stats': result.chapter_stats,
        'recommendations': result.recommendations
    })


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    results = Result.objects.filter(user=request.user)

    total_tests = results.count()

    avg_score = 0
    best_score = 0

    if total_tests > 0:
        avg_score = sum([(r.score / r.total) * 100 for r in results]) / total_tests
        best_score = max([r.score for r in results])

    if request.method == 'POST':

        # image update
        if request.FILES.get('image'):
            profile.image = request.FILES['image']

        # user fields
        request.user.email = request.POST.get('email')

        # profile fields
        profile.full_name = request.POST.get('full_name')
        profile.student_class = request.POST.get('student_class')
        profile.college = request.POST.get('college')
        profile.phone = request.POST.get('phone')

        request.user.save()
        profile.save()

    return render(request, 'profile.html', {
        'profile': profile,
        'results': results,
        'total_tests': total_tests,
        'avg_score': round(avg_score, 1),
        'best_score': best_score
    })

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':

        # update fields
        request.user.email = request.POST.get('email')

        profile.full_name = request.POST.get('full_name')
        profile.student_class = request.POST.get('student_class')
        profile.college = request.POST.get('college')
        profile.phone = request.POST.get('phone')

        request.user.save()
        profile.save()

        return redirect('profile')

    return render(request, 'edit_profile.html', {'profile': profile})


@login_required
def delete_result(request, id):
    if request.method == "POST":
        result = get_object_or_404(Result, id=id, user=request.user)
        result.delete()
    return redirect('dashboard')