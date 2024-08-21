import aiohttp

from crud.answer import answer_crud

YANDEX_HEADERS = {
    'Authorization': 'Api-Key AQVN2Vd-gMlDAjVPAKNMAYxb7t6JpNOag60-Mcgz',
    'x-folder-id': 'b1g2ahktcv1255vqabvd',
    'Content-Type': 'application/json'}


async def org_hints(organization, session):
    grouped_answers = await answer_crud.get_grouped_answers(
        org_id=organization.id,
        session=session
    )

    ratings = []
    for group in grouped_answers:
        if group[1] == 'Range':
            ratings.append(
                {
                    'text': f'вопрос: {group[0]};'
                            f'оценка: {group[2]} из 10',
                    'role': 'user'
                }
            )
        else:
            ratings.append(
                {
                    'text': f'вопрос: {group[0]};'
                            f'оценка: {(group[2] + 1) * 5} из 10',
                    'role': 'user'
                }
            )

    data = {
        'modelUri': 'gpt://b1g2ahktcv1255vqabvd/yandexgpt',
        'messages': [
            {
                'text': 'Ты аналитик, который помогает компании. '
                        'Дай совет на основе средней оценки в формате вопрос:оценка + твой совет',
                'role': 'system'
            },
            *ratings
        ],
        'completionOptions': {
            'stream': False,
            'maxTokens': 500,
            'temperature': 0.4
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
                json=data,
                headers=YANDEX_HEADERS
        ) as resp:
            response = await resp.json()
            msg = response['result']['alternatives'][0]['message']['text']
            return {'text': msg}
