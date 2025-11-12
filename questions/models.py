import uuid
from django.db import models
from django.core.validators import MinLengthValidator


class Question(models.Model):
    """
    Модель вопроса.

    Поля:
        text (TextField): Текст вопроса. Не может быть пустым; проверяется
            через MinLengthValidator(1).
        created_at (DateTimeField): Дата и время создания вопроса (устанавливается автоматически).

    Методы:
        __str__(): Возвращает строковое представление вопроса в формате
            'Q#<id>: <первые 50 символов текста>'.
    """
    text: str = models.TextField(
        validators=[MinLengthValidator(1, message="Вопрос не может быть пустым.")],
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q#{self.pk}: {self.text[:50]}"


class Answer(models.Model):
    """
    Модель ответа на вопрос.

    Поля:
        question (ForeignKey): Ссылка на объект `Question`, к которому относится ответ.
        user_id (UUIDField): UUID пользователя, создавшего ответ. По умолчанию
            генерируется с помощью `uuid.uuid4`.
        text (TextField): Текст ответа. Не может быть пустым; проверяется
            через MinLengthValidator(1).
        created_at (DateTimeField): Дата и время создания ответа (устанавливается автоматически).

    Методы:
        __str__(): Возвращает строковое представление ответа в формате
            'A#<id> (Q#<id вопроса>)'.
    """
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    user_id: uuid.UUID = models.UUIDField(default=uuid.uuid4)
    text: str = models.TextField(
        validators=[MinLengthValidator(1, message="Ответ не может быть пустым.")],
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A#{self.pk} (Q#{self.question_id})"