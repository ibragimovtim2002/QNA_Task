# questions/models.py
import uuid
from django.db import models


class Question(models.Model):
    """
    Модель вопроса.

    Поля:
        text (TextField): Текст вопроса.
        created_at (DateTimeField): Дата и время создания (устанавливается автоматически).
    """
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q#{self.pk}: {self.text[:50]}"


class Answer(models.Model):
    """
    Модель ответа.

    Поля:
        question (ForeignKey): Ссылка на `Question` — связанный вопрос.
        user_id (UUIDField): UUID пользователя, создавшего ответ (по умолчанию генерируется `uuid.uuid4`).
        text (TextField): Текст ответа.
        created_at (DateTimeField): Дата и время создания (устанавливается автоматически).
    """
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    user_id = models.UUIDField(default=uuid.uuid4)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A#{self.pk} (Q#{self.question_id})"