from rest_framework import serializers
from .models import Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели `Answer`.

    Назначение:
        Преобразует объекты `Answer` в представление для API и валидирует входные данные при создании/обновлении ответов.

    Методы:
        validate_text (value): гарантирует, что поле `text` не пустое и не состоит только из пробельных символов.
    """
    class Meta:
        model = Answer
        fields = ['id', 'question_id', 'user_id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'question_id']

    def validate_text(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Текст ответа не может быть пустым")
        return value


class QuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели `Question`.

    Назначение:
        Преобразует объекты `Question` в представление для API и валидирует входные данные при создании/обновлении вопросов.
        Включает вложенные ответы с помощью `AnswerSerializer` (только для чтения).

    Поля:
        answers (AnswerSerializer): вложенный список ответов, использует `many=True` и `read_only=True`.

    Методы:
        validate_text (value): гарантирует, что поле `text` не пустое и не состоит только из пробельных символов.
    """
    answers = AnswerSerializer(many=True, read_only=True)  # вложенные ответы

    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at', 'answers']
        read_only_fields = ['id', 'created_at', 'answers']

    def validate_text(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Текст вопроса не может быть пустым")
        return value