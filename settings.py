import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Путь к проекту
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
    API_TOKEN = os.getenv('API_TOKEN', 'YOUR_BOT_TOKEN') 

    # Зададим имя базы данных
    DB_NAME = os.getenv('DB_NAME', 'quiz_bot.db')

    @property
    def DB_PATH(self):
        return os.path.join(self.BASE_DIR, self.DB_NAME)

config = Config()