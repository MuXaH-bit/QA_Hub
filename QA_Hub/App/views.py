from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from App.models import Question, Tag


def new_view(request):
    questions = Question.objects.new_questions()

    data = {
        'title': 'New Questions',
        'url': 'hot',
        'url_title': 'Hot Questions',
        'page_obj': paginate(questions, request, 10),
    }

    return render(request, 'index.html', context=data)


def hot_view(request):
    questions = Question.objects.best_questions()

    data = {
        'title': 'Hot Questions',
        'url': 'new',
        'url_title': 'New Questions',
        'page_obj': paginate(questions, request, 10),
    }

    return render(request, 'index.html', context=data)


def tag_view(request, tag):
    tag_obj = get_object_or_404(Tag, name=tag)
    questions = Question.objects.filter(tags=tag_obj)

    data = {
        "tag": tag,
        "page_obj": paginate(questions, request, 10),
    }
    return render(request, 'tag.html', context=data)


def question_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()

    data = {
        "question": question,
        "answers": answers,
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


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)  # Разбиваем на страницы по 10 элементов

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return page
