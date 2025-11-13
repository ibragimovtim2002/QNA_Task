from django.shortcuts import get_object_or_404
from .models import Question, Answer

def create_question(text: str) -> Question:
    """
    Создаёт новый вопрос.
    """
    question = Question.objects.create(text=text)
    return question

def delete_question(question_id: int):
    """
    Удаляет вопрос и все связанные ответы.
    """
    question = get_object_or_404(Question, pk=question_id)
    question.delete()

def create_answer(question_id: int, user_id: str, text: str) -> Answer:
    """
    Создаёт ответ для указанного вопроса.
    """
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer.objects.create(question=question, user_id=user_id, text=text)
    return answer

def delete_answer(answer_id: int):
    """
    Удаляет ответ по ID.
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()