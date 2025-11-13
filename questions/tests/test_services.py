import pytest
import uuid
from questions.models import Question, Answer
from questions.services import create_question, create_answer, delete_question, delete_answer

@pytest.mark.django_db
def test_create_question():
    q = create_question("Тест вопрос")
    assert q.text == "Тест вопрос"

@pytest.mark.django_db
def test_create_answer():
    q = create_question("Вопрос")
    user_id = uuid.uuid4()  # вместо "user1"
    a = create_answer(q.id, user_id, "Ответ")
    assert a.text == "Ответ"
    assert a.question.id == q.id
    assert a.user_id == user_id

@pytest.mark.django_db
def test_delete_question_cascade_answers():
    q = create_question("Вопрос")
    user1 = uuid.uuid4()
    user2 = uuid.uuid4()
    a1 = create_answer(q.id, user1, "Ответ1")
    a2 = create_answer(q.id, user2, "Ответ2")
    delete_question(q.id)
    assert not Question.objects.filter(id=q.id).exists()
    assert not Answer.objects.filter(id=a1.id).exists()
    assert not Answer.objects.filter(id=a2.id).exists()

@pytest.mark.django_db
def test_delete_answer():
    q = create_question("Вопрос")
    user_id = uuid.uuid4()
    a = create_answer(q.id, user_id, "Ответ")
    delete_answer(a.id)
    assert not Answer.objects.filter(id=a.id).exists()