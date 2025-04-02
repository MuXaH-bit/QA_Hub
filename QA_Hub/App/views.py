from django.shortcuts import render
from django.core.paginator import Paginator

def homepage_view(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'title ' + str(i),
            'id': i,
            'text': 'text' + str(i)
        })

    paginator = Paginator(questions, 10)  # Разбиваем на страницы по 10 элементов

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    data = {'page_obj': page_obj}

    return render(request, 'index.html', context=data)


def tag_view(request, tag):
    data = {
        "tag": tag,
    }
    return render(request, 'tag.html', context=data)


def question_view(request, question_id):
    data = {
        "question_id": question_id,
    }
    return render(request, 'question.html', context=data)


def login_view(request):
    return render(request, 'login.html')


def singup_view(request):
    return render(request, 'singup.html')


def settings_view(request):
    return render(request, 'settings.html')


def ask_view(request):
    return render(request, 'ask.html')
