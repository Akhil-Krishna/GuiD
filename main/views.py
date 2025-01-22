from django.shortcuts import render, get_object_or_404

from roadmap.models import RoadmapStage, UserBadge, UserProgress
from .models import CodingQuestion

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request,"main/about.html")

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import io
from django.shortcuts import render, get_object_or_404
from .models import CodingQuestion

def questions(request):
    coding_questions = CodingQuestion.objects.all()
    return render(request, 'main/questions.html', {'coding_questions': coding_questions})

def code(request, question_id):
    question = get_object_or_404(CodingQuestion, id=question_id)
    return render(request, 'main/code.html', {'question': question})
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import io
from django.shortcuts import render, get_object_or_404
from .models import CodingQuestion

@csrf_exempt
def run_code(request):
    if request.method == "POST":
        data = json.loads(request.body)
        code = data.get("code", "")
        question_id = data.get("questionId")
        
        try:
            question = CodingQuestion.objects.get(id=question_id)
            test_cases = question.test_cases
            test_results = []
            
            for test_case in test_cases:
                # Capture output
                old_stdout = sys.stdout
                new_stdout = io.StringIO()
                sys.stdout = new_stdout
                
                try:
                    # Prepare the test inputs
                    test_inputs = test_case.get('input', '').split('\n')
                    input_iterator = iter(test_inputs)
                    
                    # Modified code to handle multiple inputs
                    modified_code = f"""
# Create an input iterator
_input_values = {test_inputs}
_input_iterator = iter(_input_values)

# Override input function
def input():
    try:
        return next(_input_iterator)
    except StopIteration:
        raise EOFError("Not enough input values provided")

# User's code starts here
{code}
"""
                    # Execute the code
                    exec_globals = {}
                    exec(modified_code, exec_globals)
                    
                    # Get the output
                    output = new_stdout.getvalue().strip()
                    expected_output = test_case.get('output', '').strip()
                    
                    # Compare output
                    test_passed = output == expected_output
                    test_results.append({
                        'passed': test_passed,
                        'input': test_case.get('input', ''),
                        'expected': expected_output,
                        'actual': output,
                        'error': '' if test_passed else 'Output does not match expected result'
                    })
                    
                except Exception as e:
                    test_results.append({
                        'passed': False,
                        'input': test_case.get('input', ''),
                        'expected': test_case.get('output', ''),
                        'actual': '',
                        'error': str(e)
                    })
                finally:
                    sys.stdout = old_stdout
            
            # Calculate overall results
            passed_tests = sum(1 for result in test_results if result['passed'])
            total_tests = len(test_results)
            
            return JsonResponse({
                'testResults': test_results,
                'summary': {
                    'passed': passed_tests,
                    'total': total_tests,
                    'success': passed_tests == total_tests
                }
            })
            
        except CodingQuestion.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


#user login
# main/views.py
# main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, SignInForm

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'main/sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = SignInForm()
    return render(request, 'main/sign_in.html', {'form': form})



from .models import Enrollment


# views.py

def profile(request):
    # Existing enrollment data
    enrollments = Enrollment.objects.filter(user=request.user)
    total_enrolled = enrollments.count()
    completed_courses = enrollments.filter(completed=True).count()
    
    # Get user's badges with stage information
    earned_badges = UserBadge.objects.filter(user=request.user).select_related('stage').order_by('earned_date')
    
    # Get current roadmap progress
    current_progress = UserProgress.objects.filter(
        user=request.user,
        is_stage_completed=False
    ).select_related('stage', 'current_course').first()
    
    # Calculate overall roadmap progress
    total_stages = RoadmapStage.objects.count()
    completed_stages = UserProgress.objects.filter(
        user=request.user,
        is_stage_completed=True
    ).count()
    
    # Calculate progress percentage
    progress_percentage = (completed_stages / total_stages * 100) if total_stages > 0 else 0
    
    context = {
        'user': request.user,
        'total_enrolled': total_enrolled,
        'completed_courses': completed_courses,
        'earned_badges': earned_badges,
        'current_progress': current_progress,
        'completed_stages': completed_stages,
        'total_stages': total_stages,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'main/profile_test.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/notifications.html', {'notifications': user_notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')


#notify user

from .utils import notify_user

def notify(request):
    # Some logic
    notify_user(request.user, "You have a new job notification", "http://example.com/job")
    
    
    
    
    
    
    

from .models import Course , Slide

def courses(request):
    courses = Course.objects.all()
    return render(request, 'main/courses.html', {'courses': courses})
@login_required(login_url='sign_in')
def course_detail(request, course_id, slide_order=1):
    course = get_object_or_404(Course, pk=course_id)
    slides = course.slides.all().order_by('order')
    slide = get_object_or_404(Slide, course=course, order=slide_order)

    next_slide = slides.filter(order__gt=slide.order).first()
    prev_slide = slides.filter(order__lt=slide.order).last()

    context = {
        'course': course,
        'slide': slide,
        'next_slide': next_slide,
        'prev_slide': prev_slide,
    }
    return render(request, 'main/course_detail.html', context)




# views.py (where users start a course)

from .models import Course, Enrollment
@login_required
def start_course(request, course_id):
    course = Course.objects.get(id=course_id)
    # Create an enrollment record if it doesn't exist
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    # Redirect to the first slide (order=0)
    return redirect('course_detail', course_id=course.id, slide_order=0)

# views.py
@login_required
def complete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    enrollment.completed = True
    enrollment.save()
    return redirect('profile')











#contact
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def send_email(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        # Email content
        email_message = f"""
        New contact form submission from {name}
        
        From: {email}
        Subject: {subject}
        
        Message:
        {message}
        """
        
        try:
            send_mail(
                subject=f'New Contact Form Submission: {subject}',
                message=email_message,
                from_email=email,
                recipient_list=['akhilmavannoor@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while sending your message. Please try again later.')
        
        return redirect('send_email')
    
    return render(request, 'main/contact.html')












# views.py erorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
#boommmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main/utils/rag_utils.py

# main/views.py

# main/views.py
# main/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests
from .utilss.rag_utils import RAGProcessor

rag_processor = None

# Bot configuration
BOT_CONFIG = {
    "name": "ArK Bot",
    "creator": "Akhil Krishna",
    "website_info": {
        "name": "GuiD",
        "features": {
            # You can add your website features here
            # Example structure:
            # "feature_name": "feature_description",
            "Roadmap":"Andi poora"
        }
    }
}

def get_rag_processor():
    global rag_processor
    if rag_processor is None:
        rag_processor = RAGProcessor()
    return rag_processor

def generate_bot_introduction():
    return f"Hello! I'm {BOT_CONFIG['name']}, how can I assist you today?"

def check_special_queries(user_message):
    """Handle special queries about bot identity and website information"""
    user_message_lower = user_message.lower()
    
    # Check for creator-related questions
    if any(q in user_message_lower for q in ["who created you", "who made you", "your creator"]):
        return f"I was created by {BOT_CONFIG['creator']}."
    
    # Check for website-related questions
   
    return None

@csrf_exempt
def chat_with_llama(request):
    try:
        processor = get_rag_processor()
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        # Check for special queries first
        special_response = check_special_queries(user_message)
        if special_response:
            return JsonResponse({
                'response': special_response,
                'status': 'success',
                'used_dataset': False
            })
        
        # Check if query matches dataset
        is_similar, context = processor.find_similar_questions(user_message)
        
        if is_similar:
            prompt = f"""As {BOT_CONFIG['name']}, answer the following question using the provided context and additional knowledge if needed.

            Context from similar questions:
            {context}

            Question: {user_message}

            Please provide a complete, helpful answer:"""
        else:
            prompt = f"""As {BOT_CONFIG['name']}, please provide a complete and helpful answer to the following question:

            Question: {user_message}

            Answer:"""
        
        # Call Llama
        response = requests.post('http://localhost:11434/api/generate',
            json={
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            })
        
        if response.status_code == 200:
            return JsonResponse({
                'response': response.json()['response'],
                'status': 'success',
                'used_dataset': is_similar
            })
        else:
            return JsonResponse({
                'error': 'Failed to get response from Llama-2',
                'status': 'error'
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)
### Rather than storing content in db we can use md 

# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Course, Enrollment, Slide  # Assuming you have a Slide model
# import os
# from django.conf import settings
# def course_detail(request, course_id, slide_order=1):
#     course = get_object_or_404(Course, pk=course_id)
#     slides = course.slides.all().order_by('order')
#     slide = get_object_or_404(Slide, course=course, order=slide_order)

#     # Determine the correct content file path based on course and slide order
#     if course_id==1:
#         course_slug="Django"
#     elif course_id==2:
#         course_slug="React"
#     content_dir = os.path.join('course_content', course_slug)  # Use course slug for organization
#     content_file = f'slide{slide_order}.md'  # Assuming Markdown format
#     content_path = os.path.join('course_content', 'Django', f'slide{slide_order}.md')

#     # Read content from the file
#     with open(f"static/main/course_content/Django/slide{slide_order}.md", 'r') as f:
#         slide_content = f.read()

#     next_slide = slides.filter(order__gt=slide.order).first()
#     prev_slide = slides.filter(order__lt=slide.order).last()

#     context = {
#         'course': course,
#         'slide': slide,
#         'slide_content': slide_content,  # Add slide_content to context
#         'next_slide': next_slide,
#         'prev_slide': prev_slide,
#     }
#     return render(request, 'main/course_detail.html', context)




# # views.py (where users start a course)

# from .models import Course, Enrollment

# def start_course(request, course_id):
#     course = Course.objects.get(id=course_id)
#     # Create an enrollment record if it doesn't exist
#     enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
#     # Redirect to the first slide (order=0)
#     return redirect('course_detail', course_id=course.id, slide_order=0)
 

# # views.py
# def complete_course(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
#     enrollment.completed = True
#     enrollment.save()
#     return redirect('profile')
