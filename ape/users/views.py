from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as auth_logout
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .models import *
from .forms import CreateUserForm
from .forms import ProfileUpdateForm
from django.utils import timezone
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import QuestionForm, ChoiceFormSet
from django.shortcuts import render, get_object_or_404
from .models import Course, Question, Choice, Profile, QuizResult, Score, QUESTION_TYPES





# Create your views here.

def calculate_percentage_score(num_correct, num_questions):
    if num_questions == 0:
        return 0
    return int(num_correct / num_questions * 100)

def base(request):
    return render(request, 'users/base.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('base')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was successfully created for ' + username)

                # Create a new profile object for the user
                profile = Profile.objects.create(user=user, full_name=form.cleaned_data.get('full_name'), email=form.cleaned_data.get('email'))
                profile.full_name = form.cleaned_data.get('full_name')
                profile.email = form.cleaned_data.get('email')
                profile.save()
                 
                # Determine which login page to redirect to based on the user's selection
                if form.cleaned_data.get('user_type') == 'lecturer':
                    login_url = reverse('login1')
                else:
                    login_url = reverse('login')

                return HttpResponseRedirect(login_url + '?username=' + username)
        
        context = {'form': form}
        return render(request, 'users/signup.html', context)


def login1(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    code = request.POST.get('lecturer_code')

    if request.method == 'POST' and password and code and code == '12345':
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.warning(request, 'Wrong username or password')
            return render(request, 'users/login1.html', {'username': username})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # get the first course object
            course = Course.objects.first()
            return redirect('lec', course_id=course.id)

        else:
            messages.warning(request, 'Wrong username or password')
    elif request.method == 'POST' and code != '12345':
        messages.warning(request, 'Wrong code')

    context = {'username': username}
    return render(request, 'users/login1.html', context)





def loginPage(request):
    if request.user.is_authenticated:
        return redirect('base')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('base')
            else:
                messages.info(request, 'Username OR Password is Incorrect')
    context = {}
    return render(request, 'users/login.html', context)


   
def logout(request):
    auth_logout(request)
    return redirect('login')


    
def field_study(request):
    return render(request, 'users/field_study.html')

def about(request):
    return render(request, 'users/about.html')

@login_required(login_url='login')
def cs(request):
    return render(request, 'users/cs.html')

@login_required(login_url='login')
def telecom(request):
    return render(request, 'users/telecom.html')

@login_required(login_url='login')
def edusci(request):
    return render(request, 'users/edusci.html')

@login_required(login_url='login')
def eduart(request):
    return render(request, 'users/eduart.html')

@login_required(login_url='login')
def industrial(request):
    return render(request, 'users/industrial.html')

@login_required(login_url='login')
def nursing(request):
    return render(request, 'users/nursing.html')

def contact(request):
    return render(request, 'users/contact.html')

def mentor(request):
    return render(request, 'users/mentor.html')



@login_required(login_url='login')
def programming_in_c_quiz(request):
    # Retrieve the course object for Programming in C
    programming_in_c = Course.objects.get(title='Programming in C')

    # Retrieve the questions and choices for the Programming in C quiz
    quiz_questions = Question.objects.filter(course=programming_in_c)
    for i, question in enumerate(quiz_questions):
        question.choices = Choice.objects.filter(question=question)
        question.number = i + 1  # Add a `number` attribute to the question object to store the question number
        question.selected_choice_code_snippet = None

    # If the form has been submitted, process the user's answers
    if request.method == 'POST':
        # Create a dictionary to keep track of the user's answers
        user_answers = {}

        # Loop through the submitted form data and add the user's answers to the dictionary
        for key, value in request.POST.items():
            if key.startswith('question-'):
                question_id = int(key.split('-')[1])
                user_answers[question_id] = int(value)

        # Calculate the user's score
        num_correct = 0
        num_questions = len(quiz_questions)
        for question in quiz_questions:
            correct_choice = question.choices.get(is_correct=True)
            selected_choice_id = user_answers.get(question.id)
            selected_choice = question.choices.get(id=selected_choice_id) if selected_choice_id else None
            question.correct_answer = correct_choice.choice_text
            question.selected_answer = selected_choice.choice_text if selected_choice else ''
            if selected_choice == correct_choice:
                num_correct += 1
                question.is_correct = True  # Set is_correct attribute of the question object to True
            else:
                question.is_correct = False  # Set is_correct attribute of the question object to False
            
            if selected_choice and selected_choice.code_snippet:
                question.selected_choice_code_snippet = selected_choice.code_snippet

        # Save the quiz result to the database
        quiz_result = QuizResult(user=request.user, course=programming_in_c, num_correct=num_correct, num_questions=num_questions)
        quiz_result.save()

        # Render the results page
        return render(request, 'users/programming_in_c_quiz_results.html', {
            'num_correct': num_correct,
            'num_questions': num_questions,
            'quiz_questions': quiz_questions,
        })
        
        # If the form has not been submitted, render the quiz page
    return render(request, 'users/programming_in_c_quiz.html', {
        'course': programming_in_c,
        'quiz_questions': quiz_questions,
    })
    
def programming_in_c_quiz_results(request):
     course = Course.objects.get(title='Programming in C')
     questions = Question.objects.filter(course=course).order_by('question_number')
     user_choices = []
     correct_choices = []
     for question in questions:
        user_choice = request.POST.get(f'question{question.id}', None)
        user_choices.append(user_choice)
        correct_choice = Choice.objects.get(question=question, is_correct=True).choice_text
        correct_choices.append(correct_choice)
     num_correct = sum([1 if user_choice == correct_choice else 0 for user_choice, correct_choice in zip(user_choices, correct_choices)])
     percentage_score = round(num_correct / len(questions) * 100)
     Score.objects.create(course=course, score=percentage_score, user=request.user, date=timezone.now())
     results = zip(questions, user_choices, correct_choices)
     context = {'results': results, 'percentage_score': percentage_score}
     return render(request, 'users/programming_in_c_quiz_results.html', context)
 

@login_required(login_url='login')
def java_quiz(request):
    # Retrieve the course object for Jva
    Java = Course.objects.get(title='Java')

    # Retrieve the questions and choices for the Java quiz
    quiz_questions = Question.objects.filter(course=Java)
    for i, question in enumerate(quiz_questions):
        question.choices = Choice.objects.filter(question=question)
        question.number = i + 1  # Add a `number` attribute to the question object to store the question number
        question.selected_choice_code_snippet = None

    # If the form has been submitted, process the user's answers
    if request.method == 'POST':
        # Create a dictionary to keep track of the user's answers
        user_answers = {}

        # Loop through the submitted form data and add the user's answers to the dictionary
        for key, value in request.POST.items():
            if key.startswith('question-'):
                question_id = int(key.split('-')[1])
                user_answers[question_id] = int(value)

        # Calculate the user's score
        num_correct = 0
        num_questions = len(quiz_questions)
        for question in quiz_questions:
            correct_choice = question.choices.get(is_correct=True)
            selected_choice_id = user_answers.get(question.id)
            selected_choice = question.choices.get(id=selected_choice_id) if selected_choice_id else None
            question.correct_answer = correct_choice.choice_text
            question.selected_answer = selected_choice.choice_text if selected_choice else ''
            if selected_choice == correct_choice:
                num_correct += 1
                question.is_correct = True  # Set is_correct attribute of the question object to True
            else:
                question.is_correct = False  # Set is_correct attribute of the question object to False
            
            if selected_choice and selected_choice.code_snippet:
                question.selected_choice_code_snippet = selected_choice.code_snippet

        # Save the quiz result to the database
        quiz_result = QuizResult(user=request.user, course=Java, num_correct=num_correct, num_questions=num_questions)
        quiz_result.save()

        # Render the results page
        return render(request, 'users/java_quiz_results.html', {
            'num_correct': num_correct,
            'num_questions': num_questions,
            'quiz_questions': quiz_questions,
        })
        
        # If the form has not been submitted, render the quiz page
    return render(request, 'users/java_quiz.html', {
        'course': Java,
        'quiz_questions': quiz_questions,
    })
    
    
def java_quiz_results(request):
     course = Course.objects.get(title='Java')
     questions = Question.objects.filter(course=course).order_by('question_number')
     user_choices = []
     correct_choices = []
     for question in questions:
        user_choice = request.POST.get(f'question{question.id}', None)
        user_choices.append(user_choice)
        correct_choice = Choice.objects.get(question=question, is_correct=True).choice_text
        correct_choices.append(correct_choice)
     num_correct = sum([1 if user_choice == correct_choice else 0 for user_choice, correct_choice in zip(user_choices, correct_choices)])
     percentage_score = round(num_correct / len(questions) * 100)
     Score.objects.create(course=course, score=percentage_score, user=request.user, date=timezone.now())
     results = zip(questions, user_choices, correct_choices)
     context = {'results': results, 'percentage_score': percentage_score}
     return render(request, 'users/java_quiz_results.html', context)
 
   

def software_engineering_quiz(request):
    # Retrieve the course object for Software Engineering
    software_engineering = Course.objects.get(title='Software Engineering')

    # Retrieve the questions and choices for the Software Engineering quiz
    quiz_questions = Question.objects.filter(course=software_engineering)
    for i, question in enumerate(quiz_questions):
        question.choices = Choice.objects.filter(question=question)
        question.number = i + 1  # Add a `number` attribute to the question object to store the question number
        question.selected_choice_code_snippet = None

    # If the form has been submitted, process the user's answers
    if request.method == 'POST':
        # Create a dictionary to keep track of the user's answers
        user_answers = {}

        # Loop through the submitted form data and add the user's answers to the dictionary
        for key, value in request.POST.items():
            if key.startswith('question-'):
                question_id = int(key.split('-')[1])
                user_answers[question_id] = int(value)

        # Calculate the user's score
        num_correct = 0
        num_questions = len(quiz_questions)
        for question in quiz_questions:
            correct_choice = question.choices.get(is_correct=True)
            selected_choice_id = user_answers.get(question.id)
            selected_choice = question.choices.get(id=selected_choice_id) if selected_choice_id else None
            question.correct_answer = correct_choice.choice_text
            question.selected_answer = selected_choice.choice_text if selected_choice else ''
            if selected_choice == correct_choice:
                num_correct += 1
                question.is_correct = True  # Set is_correct attribute of the question object to True
            else:
                question.is_correct = False  # Set is_correct attribute of the question object to False

            if selected_choice and selected_choice.code_snippet:
                question.selected_choice_code_snippet = selected_choice.code_snippet

        # Save the quiz result to the database
        quiz_result = QuizResult(user=request.user, course=software_engineering, num_correct=num_correct, num_questions=num_questions)
        quiz_result.save()

        # Render the results page
        return render(request, 'users/software_engineering_quiz_results.html', {
            'num_correct': num_correct,
            'num_questions': num_questions,
            'quiz_questions': quiz_questions,
        })

    # If the form has not been submitted, render the quiz page
    return render(request, 'users/software_engineering_quiz.html', {
        'course': software_engineering,
        'quiz_questions': quiz_questions,
    })

def software_engineering_quiz_results(request):
    course = Course.objects.get(title='Software Engineering')
    questions = Question.objects.filter(course=course).order_by('question_number')
    user_choices = []
    correct_choices = []
    for question in questions:
        user_choice = request.POST.get(f'question{question.id}', None)
        user_choices.append(user_choice)
        correct_choice = Choice.objects.get(question=question, is_correct=True).choice_text
        correct_choices.append(correct_choice)
    num_correct = sum([1 if user_choice == correct_choice else 0 for user_choice, correct_choice in zip(user_choices, correct_choices)])
    percentage_score = round(num_correct / len(questions) * 100)
    Score.objects.create(course=course, score=percentage_score, user=request.user, date=timezone.now())
    results = zip(questions, user_choices, correct_choices)
    context = {'results': results, 'percentage_score': percentage_score}
    return render(request, 'users/software_engineering_quiz_results.html', context)


def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    full_name = request.user.profile.full_name
    
    # get percentage scores for all courses and add to context
    courses = Course.objects.all()
    course_scores = {}
    for course in courses:
        course_scores[course.id] = request.user.profile.get_percentage_score(course.id)

    # get quiz results and add to context
    quiz_results = {}
    try:
        c_course = Course.objects.get(title='Programming in C')
        c_quiz_result = QuizResult.objects.filter(user=request.user, course=c_course).order_by('-date').first()
        if c_quiz_result:
            c_percentage_score = calculate_percentage_score(c_quiz_result.num_correct, c_quiz_result.num_questions)
            quiz_results['c_quiz_percentage'] = c_percentage_score
    except Course.DoesNotExist:
        pass

    context = {
        'form': form,
        'profile': request.user.profile,
        'course_scores': course_scores,
        'quiz_results': quiz_results,
        'full_name': full_name,
    }
    return render(request, 'users/profile.html', context)



def lec(request, course_id=None):
    courses = Course.objects.all()

    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, id=course_id)
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and choice_formset.is_valid():
            question = question_form.save(commit=False)
            question.course = course
            question.save()
            choice_formset.instance = question
            choice_formset.save()
            messages.success(request, 'Question added successfully.')
            return redirect('lec', course_id=course.id)
        
    else:
        if course_id is not None:
            course = get_object_or_404(Course, id=course_id)
            question_form = QuestionForm(initial={'course': course})
        else:
            course = None
            question_form = QuestionForm()
        choice_formset = ChoiceFormSet()

    return render(request, 'users/lec.html', {
        'courses': courses,
        'course': course,
        'question_form': question_form,
        'choice_formset': choice_formset,
        'choice_formset_management_form': choice_formset.management_form,
    })



def score_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    scores = Score.objects.filter(course=course)
    context = {
        'course': course,
        'scores': scores,
    }
    return render(request, 'users/scores.html', context)

