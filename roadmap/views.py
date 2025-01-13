
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse


#myupdate


#error causing updates




from .models import RoadmapCourse,RoadmapSlide,RoadmapStage,UserProgress,RoadmapTest,TestQuestion,TestAttempt ,UserBadge
class RoadmapStageView(View):
    @method_decorator(login_required)
    def get(self, request):
        stages = RoadmapStage.objects.all()
        progress_dict = {}
        
        # Get all user progress records
        user_progresses = UserProgress.objects.filter(user=request.user)
        
        # First stage is always accessible
        first_stage = stages.first()
        if first_stage:
            progress_dict[first_stage.id] = {
                'accessible': True,
                'progress': user_progresses.filter(stage=first_stage).first()
            }
        
        # Process remaining stages
        completed_stages = 0  # Counter for completed stages
        for index, stage in enumerate(stages):
            progress = user_progresses.filter(stage=stage).first()
            accessible = False
            
            if index == 0:  # First stage is always accessible
                accessible = True
            else:  # Other stages depend on the completion of the previous stage
                previous_stage = stages[index - 1]
                previous_progress = user_progresses.filter(stage=previous_stage).first()
                accessible = previous_progress and previous_progress.is_stage_completed
            
            # Check if the current stage is completed
            if progress and progress.is_stage_completed:
                completed_stages += 1
            
            progress_dict[stage.id] = {
                'accessible': accessible,
                'progress': progress
            }
        
        # Calculate progress percentage
        total_stages = stages.count()
        progress_percentage = (completed_stages / total_stages) * 100 if total_stages > 0 else 0

        return render(request, 'roadmap/stages.html', {
            'stages': stages,
            'progress_dict': progress_dict,
            'progress_percentage': progress_percentage,
        })


#fourth
#third update




# class RoadmapCourseView(View):
#     @method_decorator(login_required)
#     def get(self, request, stage_id, course_order):
#         stage = get_object_or_404(RoadmapStage, id=stage_id)
#         course = get_object_or_404(RoadmapCourse, stage=stage, order=course_order)
#         progress, created = UserProgress.objects.get_or_create(user=request.user, stage=stage)
#         if progress.current_course != course and not progress.is_stage_completed:
#             progress.current_course = course
#             progress.save()
#         return render(request, 'roadmap/course.html', {'stage': stage, 'course': course})
#sixthee


class RoadmapCourseList(View):
    @method_decorator(login_required)
    def get(self, request, stage_id ,course_order=1):
        stage = get_object_or_404(RoadmapStage, id=stage_id)
        course_list=RoadmapCourse.objects.filter(stage=stage).values()
        
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            stage=stage,
            defaults={'current_course': None, 'current_slide': None}
        )

        # If user completed previous course but hasn't moved to next course
        if course_order == 1 and not progress.is_stage_completed:
            # Find the last incomplete course or the last course they were on
            current_course = progress.current_course
            if current_course and current_course.order > 1:
                return redirect('roadmap_course', stage_id=stage_id, course_order=current_course.order)

        # Get the requested course
        course = get_object_or_404(RoadmapCourse, stage=stage, order=course_order)
        
        # If switching to a new course, reset slide progress
        if progress.current_course != course and not progress.is_stage_completed:
            progress.current_course = course
            progress.current_slide = None
            progress.save()

        # If user has a current_slide in THIS course, redirect to that
        if progress.current_slide and progress.current_slide.course == course:
            return redirect('roadmap_slide', course_id=course.id, slide_order=progress.current_slide.order)
        
        total_slides = RoadmapSlide.objects.filter(course=course).count()
        first_slide = RoadmapSlide.objects.filter(course=course).order_by('order').first()

        
        return render(request,"roadmap/list.html",context={"course_list":course_list,
                                                           'stage': stage, 
            'course': course,
            'total_slides': total_slides,
            'first_slide': first_slide,
            'has_progress': bool(progress.current_slide and progress.current_slide.course == course),
            'progress': progress
                                                           
                                                           })
        
# views.py
class StageCourseListView(View):
    @method_decorator(login_required)
    def get(self, request, stage_id):
        stage = get_object_or_404(RoadmapStage, id=stage_id)
        courses = RoadmapCourse.objects.filter(stage=stage).order_by('order')
        
        progress, created = UserProgress.objects.get_or_create(
            user=request.user, 
            stage=stage,
            defaults={'current_course': None}
        )
        
        courses_status = []
        current_course_order = progress.current_course.order if progress.current_course else 0
        
        for course in courses:
            status = {
                'course': course,
                'status': 'locked',  # default status
            }
            
            # First course is always available
            if course.order == 1:
                status['status'] = 'start' if current_course_order == 0 else 'complete'
            # Current course
            elif course.order == current_course_order:
                status['status'] = 'in_progress'
            # Completed courses - now accessible
            elif course.order < current_course_order:
                status['status'] = 'complete'
            # Next available course
            elif course.order == current_course_order + 1:
                status['status'] = 'start'
            
            # Make completed courses clickable
            status['clickable'] = status['status'] in ['complete', 'in_progress', 'start']
            
            courses_status.append(status)
        
        return render(request, 'roadmap/stage_courses.html', {
            'stage': stage,
            'courses_status': courses_status,
            'progress': progress,
        })
        
#changing this viewbb
class RoadmapCourseView(View):
    @method_decorator(login_required)
    def get(self, request, stage_id, course_order):
        stage = get_object_or_404(RoadmapStage, id=stage_id)
        course = get_object_or_404(RoadmapCourse, stage=stage, order=course_order)

        # Get or create progress for the user
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            stage=stage,
            defaults={'current_course': None, 'current_slide': None}
        )

        # Check if reviewing a completed course
        is_review = progress.current_course and course.order < progress.current_course.order

        # Update progress for new courses
        if not is_review:
            if course_order == 1 or progress.current_course != course:
                progress.current_course = course
                progress.current_slide = None  # Reset slide for new course
                progress.save()

            # Redirect to the current slide if resuming
            if progress.current_slide and progress.current_slide.course == course:
                return redirect('roadmap_slide', course_id=course.id, slide_order=progress.current_slide.order)

        # Start from the first slide for reviews or new courses
        first_slide = RoadmapSlide.objects.filter(course=course).order_by('order').first()
        if first_slide:
            return redirect('roadmap_slide', course_id=course.id, slide_order=first_slide.order)

        # Render course details if no slides are available
        total_slides = RoadmapSlide.objects.filter(course=course).count()
        return render(request, 'roadmap/course.html', {
            'stage': stage,
            'course': course,
            'total_slides': total_slides,
            'has_progress': bool(progress.current_slide and progress.current_slide.course == course),
            'progress': progress
        })

#gpt recommended
class RoadmapSlideView(View):
    @method_decorator(login_required)
    def get(self, request, course_id, slide_order):
        course = get_object_or_404(RoadmapCourse, id=course_id)
        slide = get_object_or_404(RoadmapSlide, course=course, order=slide_order)
        slides = RoadmapSlide.objects.filter(course=course).order_by("order")
        
        progress = get_object_or_404(UserProgress, 
            user=request.user, 
            stage=course.stage
        )
        progress.current_slide = slide
        progress.save()

        prev_slide = slides.filter(order__lt=slide_order).last()
        next_slide = slides.filter(order__gt=slide_order).first()
        
        # Check if this is the last course in the stage
        is_last_course = not RoadmapCourse.objects.filter(
            stage=course.stage, order__gt=course.order
        ).exists()

        context = {
            "slide": slide,
            "prev_slide": prev_slide,
            "next_slide": next_slide,
            "is_last_course": is_last_course,
            "course": course,
        }
        return render(request, "roadmap/slide.html", context)

    @method_decorator(login_required)
    def post(self, request, course_id, slide_order):
        course = get_object_or_404(RoadmapCourse, id=course_id)
        progress = get_object_or_404(UserProgress, user=request.user, stage=course.stage)
        
        if 'complete_course' in request.POST:
            next_course = RoadmapCourse.objects.filter(
                stage=course.stage, 
                order__gt=course.order
            ).first()
            progress.current_course = next_course
            progress.current_slide = None
            progress.save()
            return redirect('stage_courses', stage_id=course.stage.id)
        
        return redirect('roadmap_slide', course_id=course_id, slide_order=slide_order)
    #fifth update



from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.db.models import Max
class RoadmapTestView(View):
    @method_decorator(login_required)
    def get(self, request, stage_id):
        stage = get_object_or_404(RoadmapStage, id=stage_id)

        # Check if user has completed all courses in the stage
        user_progress = get_object_or_404(UserProgress, user=request.user, stage=stage)
        last_course = RoadmapCourse.objects.filter(stage=stage).order_by('-order').first()

        if not user_progress.current_course or user_progress.current_course.order < last_course.order:
            messages.error(request, "Please complete all courses before taking the test.")
            return redirect('roadmap_stages')

        test = get_object_or_404(RoadmapTest, stage=stage)
        questions = list(TestQuestion.objects.filter(test=test))
        total_questions = len(questions)

        # Get current question number from session or start with the first question
        current_question_idx = request.session.get(f'test_{test.id}_current_question', 0)

        # Get previously saved answers from session
        saved_answers = request.session.get(f'test_{test.id}_answers', {})

        # Get the current question
        current_question = questions[current_question_idx]

        # Check if this is the first/last question
        is_first_question = current_question_idx == 0
        is_last_question = current_question_idx == total_questions - 1

        # Add options for the current question
        options = [
            ('A', current_question.option_a),
            ('B', current_question.option_b),
            ('C', current_question.option_c),
            ('D', current_question.option_d),
        ]

        context = {
            'stage': stage,
            'question': current_question,
            'question_number': current_question_idx + 1,
            'total_questions': total_questions,
            'is_first_question': is_first_question,
            'is_last_question': is_last_question,
            'selected_option': saved_answers.get(str(current_question.id)),
            'options': options,  # Pass the options to the template
        }

        return render(request, 'roadmap/test_question.html', context)
    @method_decorator(login_required)
    def post(self, request, stage_id):
        stage = get_object_or_404(RoadmapStage, id=stage_id)
        test = get_object_or_404(RoadmapTest, stage=stage)
        questions = list(TestQuestion.objects.filter(test=test))
        total_questions = len(questions)

        # Keep the navigation logic as is until submission...
        if 'next' in request.POST or 'previous' in request.POST:
            # ... (keep existing navigation code) ...
            # Save current answer
            current_question_idx = request.session.get(f'test_{test.id}_current_question', 0)
            current_question = questions[current_question_idx]
            
            # Get answers dict from session or create new
            saved_answers = request.session.get(f'test_{test.id}_answers', {})
            
            # Save current answer if provided
            selected_option = request.POST.get('selected_option')
            if selected_option:
                saved_answers[str(current_question.id)] = selected_option
                request.session[f'test_{test.id}_answers'] = saved_answers

            # Update current question index
            if 'next' in request.POST and current_question_idx < total_questions - 1:
                request.session[f'test_{test.id}_current_question'] = current_question_idx + 1
            elif 'previous' in request.POST and current_question_idx > 0:
                request.session[f'test_{test.id}_current_question'] = current_question_idx - 1
            
            
            return redirect('roadmap_test', stage_id=stage_id)

        # Modified submission handling
        elif 'submit' in request.POST:
            saved_answers = request.session.get(f'test_{test.id}_answers', {})
            
            # Save the last answer if provided
            current_question_idx = request.session.get(f'test_{test.id}_current_question', 0)
            current_question = questions[current_question_idx]
            selected_option = request.POST.get('selected_option')
            if selected_option:
                saved_answers[str(current_question.id)] = selected_option

            # Calculate score
            correct_answers = 0
            question_results = []  # Track individual question results
            for question in questions:
                is_correct = saved_answers.get(str(question.id)) == question.correct_option
                if is_correct:
                    correct_answers += 1
                question_results.append({
                    'question': question,
                    'selected': saved_answers.get(str(question.id)),
                    'correct': is_correct
                })

            score_percentage = (correct_answers / total_questions) * 100
            passed = score_percentage >= test.passing_score

            # Record the attempt
            TestAttempt.objects.create(
                user=request.user,
                test=test,
                score=score_percentage,
                passed=passed
            )

            # Get previous best score
            best_score = TestAttempt.objects.filter(
                user=request.user,
                test=test
            ).aggregate(Max('score'))['score__max']

            # Clear test session data
            for key in list(request.session.keys()):
                if key.startswith(f'test_{test.id}'):
                    del request.session[key]

            # Update progress if passed
            if passed:
                user_progress = get_object_or_404(UserProgress, user=request.user, stage=stage)
                user_progress.is_stage_completed = True
                user_progress.badge_earned = True
                user_progress.save()

                # Create badge record
                UserBadge.objects.get_or_create(
                    user=request.user,
                    stage=stage
                )

            # Get next stage if exists
            next_stage = RoadmapStage.objects.filter(id__gt=stage.id).first()
            
            # Prepare improvement tips
            tips = [
                "Review the course material carefully",
                "Take notes during the courses",
                "Practice with similar examples",
                "Focus on understanding concepts rather than memorizing"
            ]

            return render(request, 'roadmap/test_result.html', {
                'stage': stage,
                'score': score_percentage,
                'passed': passed,
                'best_score': best_score,
                'passing_score': test.passing_score,
                'next_stage': next_stage,
                'tips': tips if not passed else None,
                'badge_image': stage.badge_image if passed else None,
                'total_questions': total_questions,
                'correct_answers': correct_answers,
            })

        return redirect('roadmap_test', stage_id=stage_id)
    
    
    
    
    
## AI enhancer for slides    
    
    
import logging
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

def chat_with_llama(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message')
        
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2:1b",
                "prompt": user_message,
                "stream": False
            })
        
        if response.status_code == 200:
            return JsonResponse({
                'response': response.json()['response'],
                'status': 'success'
            })
        else:
            logger.error(f"Llama API Error: {response.status_code} - {response.text}")
            return JsonResponse({
                'error': 'Failed to get response from Llama API',
                'status': 'error'
            }, status=500)
            
    except Exception as e:
        logger.exception("Error in chat_with_llama view")
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)
