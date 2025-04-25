import json
import logging 
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import Message

from user import User
from db_handler import DBHandler, MongoDBHandler
from logger import create_logger

logger = create_logger('valentine_bot', 'valentine_bot.log')
users : dict[str, User] = {}

def get_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def get_messag_texts():
    with open('texts.json', 'r', encoding='utf-8') as f:
        return json.load(f)

dp = Dispatcher()

config = get_config()
texts = get_messag_texts()

db_handler = MongoDBHandler(
    db_name = config['db_name'],
    db_url = config['db_url'],
)


@dp.message(CommandStart())
async def start_command(message: Message):
    user = db_handler.get_user(
        user_id = message.from_user.id,
        username = message.from_user.username
    )
    users[message.from_user.id] = user
    logger.info(f'found user: {user}')

    await message.answer(
        texts['start_message'].format(
            username = message.from_user.username,
        )
    )

@dp.message('/help')
async def help_command(message: Message):
    await message.answer(texts['help_message'])
    

async def main():
    bot = Bot(token=config['token'])
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    logger.info('started polling...')
    