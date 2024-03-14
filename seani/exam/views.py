from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import CandidateForm
from django.contrib.auth.models import User

from.models import Exam

# Create your views here.

def home(request):
    user = request.user
    return render(request, 'exam/home.html', {'user': user})

def question(request, m_id, q_id =1):
    exam = request.user.exam
    if request.method == 'POST':
        answer = request.POST['answer']
        questions = exam.breakdown_set.filter(question__module_id=m_id)
        question = questions[q_id - 1]
        question.answer = answer
        question.save()
        return redirect('exam:question', m_id, q_id + 1)
    try:
        questions = exam.breakdown_set.filter(question__module_id=m_id)
        # questions = user.exam.questions.filter(module_id=m_id)
        question = questions[q_id - 1].question
        answer = questions[q_id - 1].answer
        return render(request, 'exam/question.html', {
            'question': question,
            'answer': answer,
            'm_id': m_id,
            'q_id': q_id,
        })
    except IndexError:
        return redirect('exam:home')


def add_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            
            #recibir datos

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            career = form.cleaned_data['career']
            stage = form.cleaned_data['stage']

            #crear usuario
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()


            #crear examen
            exam = Exam.objects.create(
                user=user, 
                career=career, 
                stage=stage)
            
            exam.set_modules()
            exam.set_questions()
            return HttpResponse('Usuario y examen creado!')


            #llenar examen
        
        

    form = CandidateForm()
    return render(request, 'exam/add_candidate.html',
                  {'form': form})