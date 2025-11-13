from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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


class AnswerViewSet(viewsets.GenericViewSet):
    """
    ViewSet для модели Answer.

    Назначение:
        Предоставляет ограниченный набор операций REST API для объектов Answer:
        получение одного объекта (retrieve) и удаление (destroy).

    Атрибуты:
        queryset (QuerySet): Набор всех ответов (`Answer.objects.all()`).
        serializer_class (Serializer): Сериализатор, используемый для представления и валидации (`AnswerSerializer`).

    Методы:
        retrieve(request, pk): Возвращает сериализованные данные ответа. Статус HTTP 200 при успехе, 404 если не найден.
        destroy(request, pk): Удаляет ответ. Статус HTTP 204 при успешном удалении, 404 если не найден.

    Примечание:
        Использует `get_object_or_404` для получения экземпляра и стандартные ответы DRF через `Response`.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def retrieve(self, request, pk=None):
        answer = get_object_or_404(Answer, pk=pk)
        serializer = self.get_serializer(answer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        answer = get_object_or_404(Answer, pk=pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)