from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, create_answer_for_question

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/answers/', create_answer_for_question, name='create_answer'),
]