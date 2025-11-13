from rest_framework import viewsets

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Question.

    Назначение:
        Предоставляет стандартные CRUD-операции через REST API для объектов Question:
        list, retrieve, create, update, partial_update, destroy.

    Атрибуты:
        queryset (QuerySet): Набор вопросов, отсортированный по убыванию даты создания.
        serializer_class (Serializer): Сериализатор, используемый для валидации и представления данных (QuestionSerializer).

    Примечание:
        Вложенные ответы включаются через `QuestionSerializer` (read-only).
    """
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer