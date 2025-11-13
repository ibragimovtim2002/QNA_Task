import pytest
import uuid
from rest_framework.test import APIClient
from questions.models import Question, Answer

@pytest.mark.django_db
def test_create_question_api():
    client = APIClient()
    url = "/api/questions/"
    data = {"text": "Новый вопрос"}
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["text"] == "Новый вопрос"

@pytest.mark.django_db
def test_delete_question_api():
    client = APIClient()
    q = Question.objects.create(text="Удаляемый вопрос")
    url = f"/api/questions/{q.id}/"
    response = client.delete(url)
    assert response.status_code == 204
    assert not Question.objects.filter(id=q.id).exists()

@pytest.mark.django_db
def test_create_answer_api():
    client = APIClient()
    q = Question.objects.create(text="Вопрос")
    url = f"/api/questions/{q.id}/answers/"
    user_id = str(uuid.uuid4())  # валидный UUID в виде строки
    data = {"user_id": user_id, "text": "Ответ"}
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["text"] == "Ответ"

@pytest.mark.django_db
def test_delete_answer_api():
    client = APIClient()
    q = Question.objects.create(text="Вопрос")
    user_id = uuid.uuid4()
    a = Answer.objects.create(question=q, user_id=user_id, text="Ответ")
    url = f"/api/answers/{a.id}/"
    response = client.delete(url)
    assert response.status_code == 204
    assert not Answer.objects.filter(id=a.id).exists()