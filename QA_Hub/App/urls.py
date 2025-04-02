from django.urls import path
from .views import (
    homepage_view,
    tag_view,
    question_view,
    login_view,
    singup_view,
    ask_view,
    settings_view
    )

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('hot/', homepage_view, name='hot'),
    path('tag/<tag>', tag_view, name='tag'),
    path('question/<question_id>/', question_view, name='question'),
    path('login/', login_view, name='login'),
    path('singup/', singup_view, name='singup'),
    path('ask/', ask_view, name='ask'),
    path('settings/', settings_view, name='settings'),
]
