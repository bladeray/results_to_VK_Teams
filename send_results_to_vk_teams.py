import os

import requests
from bot.bot import Bot


def get_launch_id(project_id: int) -> int:
    resp = requests.get(
        url=f"{os.environ['bamboo_ALLURE_BASE_URL']}api/rs/launch",
        params={'projectId': project_id, 'sort.sorted': True},
        headers={'Authorization': f'Api-Token {os.environ["bamboo_ALLURE_TOKEN_SECRET"]}'},
        verify=False
    )
    resp.raise_for_status()
    content = resp.json().get('content')
    return content[0].get('id')


def get_launch_statistic(launch_id: str) -> str:
    resp = requests.get(
        url=f'{os.environ["bamboo_ALLURE_BASE_URL"]}api/rs/launch/{launch_id}/statistic',
        headers={'Authorization': f'Api-Token {os.environ["bamboo_ALLURE_TOKEN_SECRET"]}'},
        verify=False
    )
    resp.raise_for_status()
    return ', '.join([f'{stat.get("count")} {stat.get("status")}' for stat in resp.json()])


current_launch_id = get_launch_id(project_id=int(os.environ['bamboo_ALLURE_PROJECT_ID']))

TOKEN = os.environ['bamboo_VK_BOT_TOKEN_SECRET']

bot = Bot(token=TOKEN)
bot.api_base_url = os.environ['bamboo_VK_API_URL']

message = f'''*Service*: {os.environ['bamboo_PROJECT_NAME']} | Marketplace Team
*Branch*: {os.environ['bamboo_planRepository_branchName']}
*Build*: {os.environ['bamboo_resultsUrl']}
*Allure TestOps*: {os.environ['bamboo_ALLURE_BASE_URL']}launch/{current_launch_id}
*Status*: {'❌ Failed' if int(os.environ['PYTEST_EXIT_CODE']) > 0 else '✅ Success'}
*Statistic*: {get_launch_statistic(str(current_launch_id))}'''

bot.send_text(chat_id='26988@chat.agent', text=message, parse_mode='MarkdownV2')
