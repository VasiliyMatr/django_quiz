from django import forms

class QuestionForm(forms.Form):
    question_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите текст вопроса',
            'rows': 3
        })
    )
    answer1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    answer2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    answer3 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    answer4 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    correct_answer = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True,
        error_messages={
            'required': 'Выберите правильный ответ!'
        }
    )
