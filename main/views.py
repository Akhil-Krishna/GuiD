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
        user_code = data.get("code", "")
        question_id = data.get("questionId")
        
        try:
            question = CodingQuestion.objects.get(id=question_id)
            test_cases = question.test_cases
            test_results = []
            
            # Prepare the environment
            namespace = {}
            
            # Add necessary helper functions based on the question type
            helper_code = """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
def create_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

def linked_list_to_array(head):
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result
"""
            # Execute helper code
            exec(helper_code, namespace)
            
            # Execute user's code
            try:
                exec(user_code, namespace)
            except Exception as e:
                return JsonResponse({
                    'error': f'Code execution error: {str(e)}',
                    'testResults': [],
                    'summary': {'passed': 0, 'total': len(test_cases), 'success': False}
                }, status=400)

            for test_case in test_cases:
                # Capture output
                old_stdout = sys.stdout
                new_stdout = io.StringIO()
                sys.stdout = new_stdout
                
                try:
                    input_data = test_case.get('input', '')
                    expected_output = test_case.get('output', '')
                    
                    # Handle different question types
                    if "Two Sum" in question.title:
                        nums = eval(input_data.split('\n')[0])
                        target = int(input_data.split('\n')[1])
                        result = namespace['twoSum'](nums, target)
                        actual_output = str(result)
                    
                    elif "Longest Substring" in question.title:
                        s = input_data.strip()
                        result = namespace['lengthOfLongestSubstring'](s)
                        actual_output = str(result)
                    
                    elif "Reverse Linked List" in question.title:
                        arr = eval(input_data)
                        head = namespace['create_linked_list'](arr)
                        result = namespace['reverseList'](head)
                        actual_output = str(namespace['linked_list_to_array'](result))
                    
                    elif "Maximum Subarray" in question.title:
                        nums = eval(input_data)
                        result = namespace['maxSubArray'](nums)
                        actual_output = str(result)
                    
                    elif "Merge Two Sorted List" in question.title:
                        arr1, arr2 = map(eval, input_data.split('\n'))
                        l1 = namespace['create_linked_list'](arr1)
                        l2 = namespace['create_linked_list'](arr2)
                        result = namespace['mergeTwoLists'](l1, l2)
                        actual_output = str(namespace['linked_list_to_array'](result))
                    
                    elif "String is Palindrome" in question.title:
                        s = input_data.strip()
                        result = namespace['isPalindrome'](s)
                        actual_output = str(result).lower()
                    
                    # Compare output
                    test_passed = str(actual_output).strip() == str(expected_output).strip()
                    test_results.append({
                        'passed': test_passed,
                        'input': input_data,
                        'expected': expected_output,
                        'actual': actual_output,
                        'error': '' if test_passed else 'Output does not match expected result'
                    })
                    
                except Exception as e:
                    test_results.append({
                        'passed': False,
                        'input': test_case.get('input', ''),
                        'expected': expected_output,
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
from .models import customuser
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
    
    #leaderboard
    top_users = customuser.objects.order_by('-xp')[:10]
    xpp=request.user.xp
    context = {
        'user': request.user,
        'total_enrolled': total_enrolled,
        'completed_courses': completed_courses,
        'earned_badges': earned_badges,
        'current_progress': current_progress,
        'completed_stages': completed_stages,
        'total_stages': total_stages,
        'progress_percentage': progress_percentage,
        'topusers': top_users,
        'xp':xpp
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









from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect

def send_email(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to send a message.')
            return redirect('login')
        
        name = request.POST['name']
        subject = request.POST['subject']
        message = request.POST['message']
        user_email = request.user.email  # Extracting email from the logged-in user
        
        # Email content
        email_message = f"""
        New contact form submission from {name}
        
        From: {user_email}
        Subject: {subject}
        
        Message:
        {message}
        """
        
        try:
            send_mail(
                subject=f'New Contact Form Submission: {subject}',
                message=email_message,
                from_email=user_email,
                recipient_list=['a.k.3.0.0.2.3.0.3.1@gmail.com'],
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
#dfghjklkjhgfdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

# main/views.py
# main/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from groq import Groq
from .utilss.rag_utils import RAGProcessor
from django.conf import settings

# Initialize Groq client - you'll need to set this environment variable
import os
groq_client = Groq(api_key=settings.GROQ_API_KEY)

rag_processor = None

# Bot configuration
BOT_CONFIG = {
    "name": "Dr.FrnD",
    "creator": "Akhil Krishna",
    "website_info": {
        "name": "GuiD",
        "features": {
            "Roadmap": "nothing"
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
    
    if any(q in user_message_lower for q in ["who created you", "who made you", "your creator"]):
        return f"I was created by {BOT_CONFIG['creator']}."
    
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
        
        # Call Groq API
        completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are {BOT_CONFIG['name']}, a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",  # You can also use "llama2-70b-4096"
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            stream=False
        )
        
        return JsonResponse({
            'response': completion.choices[0].message.content,
            'status': 'success',
            'used_dataset': is_similar
        })
            
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
