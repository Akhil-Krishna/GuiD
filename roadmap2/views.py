from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Stage, Course, Slide, UserProgress

# Views

def roadmap_home(request):
    stages = Stage.objects.all()
    return render(request, 'roadmap2/home.html', {'stages': stages})


def stage_detail(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)
    courses = stage.courses.all()
    return render(request, 'roadmap2/stage_detail.html', {'stage': stage, 'courses': courses})


def course_detail(request, stage_id, course_id):
    stage = get_object_or_404(Stage, id=stage_id)
    course = get_object_or_404(Course, id=course_id, stage=stage)
    slides = course.slides.all()
    user_progress = UserProgress.objects.get(user=request.user)

    if user_progress.current_stage != stage or user_progress.current_course != course:
        return HttpResponseForbidden("Access Denied")

    current_slide = slides[user_progress.current_slide - 1]
    return render(request, 'roadmap2/course_detail.html', {
        'stage': stage,
        'course': course,
        'slides': slides,
        'current_slide': current_slide,
        'user_progress': user_progress,
    })


def next_slide(request, stage_id, course_id):
    user_progress = UserProgress.objects.get(user=request.user)
    user_progress.move_to_next_slide()
    user_progress.save()
    return redirect('course_detail', stage_id=stage_id, course_id=course_id)


def complete_course(request, stage_id, course_id):
    user_progress = UserProgress.objects.get(user=request.user)
    user_progress.move_to_next_course()
    user_progress.save()
    return redirect('stage_detail', stage_id=stage_id)
