import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

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

    Методы:
        create(self, request, *args, **kwargs): Создание вопроса с логгированием
        destroy(self, request, *args, **kwargs): Удаляет вопрос и все связанные ответы с логгированием

    Примечание:
        Вложенные ответы включаются через `QuestionSerializer` (read-only).
    """
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        """
        Создаёт новый объект Question через API.

        Аргументы:
            request (rest_framework.request.Request): HTTP-запрос с данными нового вопроса.
            *args: дополнительные позиционные аргументы.
            **kwargs: дополнительные именованные аргументы.

        Поведение:
            - Валидирует входные данные через сериализатор.
            - Создаёт объект Question в базе данных.
            - Логирует процесс создания вопроса.
            - Возвращает Response со статусом 201 при успешном создании.

        Returns:
            rest_framework.response.Response: сериализованные данные созданного вопроса и заголовки ответа.

        Raises:
            serializers.ValidationError: если входные данные невалидны.
        """
        logger.info(f"Попытка создать вопрос: {request.data}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info(f"Вопрос создан успешно: id={serializer.instance.id}")
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        """
       Удаляет объект Question и все связанные с ним ответы через API.

       Аргументы:
           request (rest_framework.request.Request): HTTP-запрос для удаления.
           *args: дополнительные позиционные аргументы.
           **kwargs: дополнительные именованные аргументы.

       Поведение:
           - Получает объект Question по PK через `self.get_object()`.
           - Логирует попытку удаления.
           - Выполняет удаление объекта и всех связанных Answer через `self.perform_destroy`.
           - Логирует успешное удаление.

       Returns:
           rest_framework.response.Response: пустой ответ со статусом HTTP 204 (No Content).

       Raises:
           Http404: если объект Question с указанным PK не найден.
       """
        question = self.get_object()
        logger.info(f"Попытка удалить вопрос id={question.id}")
        self.perform_destroy(question)
        logger.info(f"Вопрос id={question.id} и все ответы удалены")
        return Response(status=status.HTTP_204_NO_CONTENT)


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

logger = logging.getLogger(__name__)
@api_view(['POST'])
def create_answer_for_question(request, question_id):
    """
    Создаёт ответ для вопроса с указанным `question_id`.

    Параметры:
        request (rest_framework.request.Request): HTTP-запрос с JSON-данными. Ожидаемые поля в теле запроса:
            - user_id (UUID): идентификатор пользователя, создающего ответ;
            - text (str): текст ответа.
        question_id (int|str): PK вопроса, к которому добавляется ответ.

    Поведение:
        1. Находит объект `Question` по `question_id` или возвращает HTTP 404, если не найден.
        2. Создаёт `AnswerSerializer` для валидации входных данных.
        3. Если данные валидны — создаёт объект `Answer`, логирует создание и возвращает ответ со статусом HTTP 201.
        4. Если валидация не проходит — логирует ошибки и возвращает HTTP 400 с описанием ошибок.

    Возвращает:
        rest_framework.response.Response:
            - 201 Created с сериализованными данными ответа при успешном создании;
            - 400 Bad Request с ошибками валидации при некорректных данных;
            - 404 Not Found если вопрос не найден.

    """
    logger.info(f"Получен запрос на создание ответа для вопроса {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    serializer = AnswerSerializer(data=request.data)
    if serializer.is_valid():
        answer = Answer.objects.create(
            question=question,
            user_id=serializer.validated_data['user_id'],
            text=serializer.validated_data['text']
        )
        logger.debug(f"Ответ создан: id={answer.id}, user_id={answer.user_id}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.warning(f"Ошибка валидации при создании ответа: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)