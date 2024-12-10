from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, Vote
from .forms import QuestionForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def question_list(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  # Create a question object but don't save yet
            question.author = request.user  # Set the author to the logged-in user
            question.save()  # Save the question to the database
            return redirect('question_list')  # Redirect to the question list page after saving
    else:
        form = QuestionForm()

    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'forum/question_list.html', {'questions': questions, 'form': form})

@login_required
def add_answer(request, question_id):
    # Get the question object
    question = get_object_or_404(Question, id=question_id)

    # Handle form submission (POST request)
    if request.method == 'POST':
        content = request.POST.get('content')  # Get the content from the form
        if content:
            # Create and save the answer
            Answer.objects.create(
                question=question,
                author=request.user,  # Set the author to the logged-in user
                content=content
            )
            return redirect('question_detail', question_id=question.id)  # Redirect to the question detail page after saving the answer

    # Render the page for GET requests (display the form and question details)
    return render(request, 'forum/question_detail.html', {'question': question})

@login_required
def upvote_answer(request, question_id, answer_id):
    # Fetch the answer based on the provided ID
    answer = get_object_or_404(Answer, pk=answer_id)
    
    # Check if the user has already voted for this answer
    value = Vote.objects.filter(user=request.user, answer=answer)
    
    if value.exists():
        # If the user already voted, remove the vote (decrement the upvote)
        answer.upvote -= 1
        answer.save()
        value.delete()  # Remove the user's vote from the database
        vote_status = 'removed'
    else:
        # If the user hasn't voted yet, add the vote (increment the upvote)
        answer.upvote += 1
        answer.save()
        Vote.objects.create(user=request.user, answer=answer)  # Create a new vote
        vote_status = 'added'
    
    # Return the updated vote count and status in a JSON response
    return JsonResponse({
        'upvote': answer.upvote,
        'vote_status': vote_status
    })

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Answer.objects.create(question=question, author=request.user, content=content)
            return redirect('question_detail', question_id=question.id)

    return render(request, 'forum/question_detail.html', {'question': question})
