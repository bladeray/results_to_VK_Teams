# Скрипт, отправляющий результаты прогона автотестов в чат VK Teams.

## Environment Variables

bamboo_ в начале имени переменных окружения добавлена, т.к. переменные заведены в Bamboo CI.

Управлять тестами можно с помощью переменных окружения:

- **bamboo_ALLURE_BASE_URL**
  > Базовый URL Allure TestOps. Пример: https://allure.local/
- **bamboo_ALLURE_TOKEN_SECRET**
  > API токен для Allure
- **bamboo_ALLURE_PROJECT_ID**
  > ID проекта в Allure, который используется для получения ID запуска в Allure
- **bamboo_VK_BOT_TOKEN_SECRET**
  > API токен бота, который можно получить в @Metabot VK_Teams
- **bamboo_PROJECT_NAME**
  > Имя проекта, которое будет отображаться в сообщении в чате
- **bamboo_planRepository_branchName**
  > Стандартная переменная Bamboo, заполнять ее не нужно. Имя ветки для сообщения в чате
- **bamboo_resultsUrl**
  > Стандартная переменная Bamboo, заполнять ее не нужно. Cсылка на билд для сообщения в чате
- **PYTEST_EXIT_CODE**
  > Устанавливается в таске. Используется для отправки статуса в сообщении в чате
  
&nbsp;

Переменные задаются на Bamboo CI. Для локального использования переменных их нужно либо задать в системе, либо, что
гораздо удобнее, создать файл .env, в котором задать переменные в формате

```
bamboo_USER_LOGIN=marketplace@uitests.ru
```

&nbsp;

## Пример таски в Bamboo CI
 
Устанавливаем зависимости проекта и запускаем тесты.
Сохраняем код pytest и устанавливаем библиотеку для бота.
Запускаем скрипт

  ```
  python -m venv venv
  source venv/bin/activate 
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  playwright install --with-deps
  pytest -s tests/ --numprocesses 2 --alluredir ./allure-results
  export PYTEST_EXIT_CODE=$?
  pip install mailru-im-bot==0.0.21
  python send_results_to_vk_teams.py
  ```

&nbsp;