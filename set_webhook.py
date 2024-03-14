import os

import requests

token = os.getenv("TELEGRAM_BOT_TOKEN")
# Замените URL на адрес вашего вебхука в Telegram
webhook_url = f"https://api.telegram.org/bot{token}/setWebhook?url= https://5f02-109-93-118-125.ngrok-free.app/"

# Отправляем POST-запрос на вебхук
response = requests.post(webhook_url)

# Печатаем результат запроса
print(response.text)
