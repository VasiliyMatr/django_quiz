from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy

from .models import Question, Answer
from .forms import QuestionForm

def home(request):
    return render(request, 'quiz/home.html')

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question.objects.create(text=form.cleaned_data['question_text'])
            answers = [
                form.cleaned_data['answer1'],
                form.cleaned_data['answer2'],
                form.cleaned_data['answer3'],
                form.cleaned_data['answer4'],
            ]
            correct_index = int(form.cleaned_data['correct_answer']) - 1
            for i, text in enumerate(answers):
                Answer.objects.create(question=question, text=text, is_correct=(i == correct_index))
            return redirect('questions_list')
    else:
        form = QuestionForm()
    return render(request, 'quiz/add_question.html', {'form': form})

def questions_list(request):
    questions = Question.objects.all()
    return render(request, 'quiz/questions_list.html', {'questions': questions})

def quiz(request):
    questions = Question.objects.order_by('?')[:5]

    if request.method == 'POST':
        answered = {}
        for key in request.POST:
            if key.startswith('question_'):
                q_id = int(key.split('_')[1])
                answered[q_id] = int(request.POST[key])

        correct = 0
        for q_id, a_id in answered.items():
            if Answer.objects.get(question=q_id, id=a_id).is_correct:
                correct += 1

        return render(request, 'quiz/results.html', {
            'correct': correct,
            'total': len(questions)
        })

    return render(request, 'quiz/quiz.html', {'questions': questions})

class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('questions_list')
