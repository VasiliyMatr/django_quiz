from django.shortcuts import render, redirect
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
        error = None
        answered = {}
        for key in request.POST:
            if key.startswith('question_'):
                q_id = int(key.split('_')[1])
                try:
                    answered[q_id] = int(request.POST[key])
                except ValueError:
                    error = "Invalid answer format!"

        if len(answered) != len(questions):
            error = "Please answer all questions!"

        if error:
            return render(request, 'quiz/quiz.html', {
                'questions': questions,
                'error': error
            })

        correct = 0
        for question in questions:
            try:
                answer = Answer.objects.get(id=answered[question.id], question=question)
                if answer.is_correct:
                    correct += 1
            except (Answer.DoesNotExist, KeyError):
                pass

        return render(request, 'quiz/results.html', {
            'correct': correct,
            'total': len(questions)
        })

    return render(request, 'quiz/quiz.html', {'questions': questions})
