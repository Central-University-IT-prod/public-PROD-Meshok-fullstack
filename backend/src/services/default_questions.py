from crud.question import question_crud
from schemas.question import QuestionCreate

DEFAULT_QUESTIONS = [
    QuestionCreate(description='Оцените качество обслуживание',
                   category='Обслуживание',
                   type='Smile'),
    QuestionCreate(description='Оцените качество товара',
                   category='Товары',
                   type='Smile'),
    QuestionCreate(description='Как Вам наше помещение?',
                   category='Помещение', type='Range'),
    QuestionCreate(description='Как Вам упаковка товара?',
                   category='Товары',
                   type='Range')
]


async def add_default_questions(organization, session):
    for question in DEFAULT_QUESTIONS:
        await question_crud.create(question, session, organization)
