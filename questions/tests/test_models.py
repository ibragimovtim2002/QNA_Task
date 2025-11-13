import pytest
from django.core.exceptions import ValidationError
from questions.models import Question, Answer

@pytest.mark.django_db
def test_question_text_not_empty():
    q = Question(text="")
    with pytest.raises(ValidationError):
        q.full_clean()

@pytest.mark.django_db
def test_answer_text_not_empty():
    from questions.models import Question
    q = Question.objects.create(text="Вопрос")
    a = Answer(question=q, user_id="user1", text="")
    with pytest.raises(ValidationError):
        a.full_clean()