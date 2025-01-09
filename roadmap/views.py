
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from .models import RoadmapCourse,RoadmapSlide,RoadmapStage,UserProgress,RoadmapTest,TestQuestion,TestAttempt ,UserBadge
class RoadmapStageView(View):
    @method_decorator(login_required)
    def get(self, request):
        stages = RoadmapStage.objects.all()
        progress = {stage.id: UserProgress.objects.filter(user=request.user, stage=stage).first() for stage in stages}
        return render(request, 'roadmap/stages.html', {'stages': stages, 'progress': progress})


class RoadmapCourseView(View):
    @method_decorator(login_required)
    def get(self, request, stage_id, course_order):
        stage = get_object_or_404(RoadmapStage, id=stage_id)
        course = get_object_or_404(RoadmapCourse, stage=stage, order=course_order)
        progress, created = UserProgress.objects.get_or_create(user=request.user, stage=stage)
        if progress.current_course != course and not progress.is_stage_completed:
            progress.current_course = course
            progress.save()
        return render(request, 'roadmap/course.html', {'stage': stage, 'course': course})


class RoadmapSlideView(View):
    @method_decorator(login_required)
    def get(self, request, course_id, slide_order):
        course = get_object_or_404(RoadmapCourse, id=course_id)
        slide = get_object_or_404(RoadmapSlide, course=course, order=slide_order)
        slides = course.slides.all()
        next_slide = slides.filter(order__gt=slide.order).first()
        prev_slide = slides.filter(order__lt=slide.order).last()
        return render(request, 'roadmap/slide.html', {'slide': slide, 'next_slide': next_slide, 'prev_slide': prev_slide})

class RoadmapSlideView(View):
    @method_decorator(login_required)
    def get(self, request, course_id, slide_order, *args, **kwargs):
        course = RoadmapCourse.objects.get(id=course_id)
        slide = RoadmapSlide.objects.get(course=course, order=slide_order)
        slides = RoadmapSlide.objects.filter(course=course).order_by("order")
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
        }
        return render(request, "roadmap/slide.html", context)







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