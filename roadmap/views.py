# from django.shortcuts import render , redirect ,get_object_or_404
# from .models import Stage,Course
# # Create your views here.

# def road(request):
#     context={
#         'stages':Stage.objects.all(),
#     }
#     return render(request,"roadmap/road.html",context)

# def stage(request,id):
#     context={
#         "courses":Course.objects.filter(stage=id),
#         "id":id
#     }
#     return render(request,"roadmap/stage.html",context)


# from .models import Course , Slide
# from django.contrib.auth.decorators import login_required


# @login_required
# def course_detail(request, course_id, slide_order=1):
#     course = get_object_or_404(Course, pk=course_id)
#     slides = course.slides.all().order_by('order')
#     slide = get_object_or_404(Slide, course=course, order=slide_order)

#     next_slide = slides.filter(order__gt=slide.order).first()
#     prev_slide = slides.filter(order__lt=slide.order).last()

#     context = {
#         'course': course,
#         'slide': slide,
#         'next_slide': next_slide,
#         'prev_slide': prev_slide,
#     }
#     return render(request, 'roadmap/course_detail.html', context)




# # views.py (where users start a course)

# from .models import Course
# @login_required
# def start_course(request, course_id):
#     course = Course.objects.get(id=course_id)
#     # Create an enrollment record if it doesn't exist
#     # Redirect to the first slide (order=0)
#     return redirect('course_detail', course_id=course.id, slide_order=0)

# # views.py
# @login_required
# def complete_course(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
#     enrollment.completed = True
#     enrollment.save()
#     return redirect('')




