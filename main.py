import json
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from user import User, HeartStyle
from db_handler import DBHandler, MongoDBHandler
from logger import create_logger

from heart_props_keyboard import HeartState, heart_style_keyboard, heart_form_keyboard, heart_color_keyboard, heart_props_keyboard, heart_size_keyboard

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

@dp.message(Command('help'))
async def help_command(message: Message):
    logger.info(f'help command from user: {message.from_user.username}')
    await message.answer(texts['help_message'])

@dp.message(Command('commands'))
async def commands_command(message: Message):
    logger.info(f'commands command from user: {message.from_user.username}')
    await message.answer(texts['commands_message'])

@dp.message(Command('generate'))
async def generate_command(message: Message):
    logger.info(f'generate command from user: {message.from_user.username}')
    await message.answer(texts['generate_message'])

@dp.message(Command('show_settings'))
async def show_settings_command(message: Message):
    logger.info(f'show_settings command from user: {message.from_user.username}')
    logger.info(f"settings: {users[message.from_user.id]}")
    user = users[message.from_user.id]
    await message.answer(
        texts['show_settings_message'].format(
            username = message.from_user.username,
            heart_style = user.heart_style,
            heart_form = user.heart_form,
            heart_color = user.heart_color,
            heart_props = user.heart_props,
            heart_size = user.heart_size,
        )
    )

@dp.message(Command('generation_setitngs'))
async def set_new_heart_command(message: Message, state: FSMContext):
    logger.info(f'set_new_heart command from user: {message.from_user.username}')
    await message.answer(texts['heart_style_message'], reply_markup=heart_style_keyboard())
    await state.set_state(HeartState.style)

@dp.callback_query(F.data.startswith('style_'))
async def heart_style_callback(callback: CallbackQuery, state: FSMContext):
    logger.info(f'heart_style_callback from user: {callback.from_user.username}')
    style = callback.data.split('_')[1]
    if style == 'back':
        await state.clear()
        return
    
    await state.update_data(style=style)

    await callback.message.answer(texts['heart_form_message'], reply_markup=heart_form_keyboard())
    await state.set_state(HeartState.form)

    await callback.answer()


@dp.callback_query(F.data.startswith('form_'))
async def heart_form_callback(callback: CallbackQuery, state: FSMContext):
    logger.info(f'heart_form_callback from user: {callback.from_user.username}')
    form = callback.data.split('_')[1]
    if form == 'back':
        await callback.message.answer(texts['heart_style_message'], reply_markup=heart_style_keyboard())
        await state.set_state(HeartState.style)
        return
    
    await state.update_data(form=form)

    await callback.message.answer(texts['heart_color_message'], reply_markup=heart_color_keyboard())
    await state.set_state(HeartState.color)

    await callback.answer()

@dp.callback_query(F.data.startswith('color_'))
async def heart_color_callback(callback: CallbackQuery, state: FSMContext):
    logger.info(f'heart_color_callback from user: {callback.from_user.username}')
    color = callback.data.split('_')[1]
    if color == 'back':
        await callback.message.answer(texts['heart_form_message'], reply_markup=heart_form_keyboard())
        await state.set_state(HeartState.form)
        return
    
    await state.update_data(color=color)

    await callback.message.answer(texts['heart_props_message'], reply_markup=heart_props_keyboard())
    await state.set_state(HeartState.props)

    await callback.answer()

@dp.callback_query(F.data.startswith('props_'))
async def heart_props_callback(callback: CallbackQuery, state: FSMContext):
    logger.info(f'heart_props_callback from user: {callback.from_user.username}')
    props = callback.data.split('_')[1]
    if props == 'back':
        await callback.message.answer(texts['heart_color_message'], reply_markup=heart_color_keyboard())
        await state.set_state(HeartState.color)
        return
    
    await state.update_data(props=props)

    await callback.message.answer(texts['heart_size_message'], reply_markup=heart_size_keyboard())
    await state.set_state(HeartState.size)

    await callback.answer()

@dp.callback_query(F.data.startswith('size_'))
async def heart_size_callback(callback: CallbackQuery, state: FSMContext):
    logger.info(f'heart_size_callback from user: {callback.from_user.username}')
    size = callback.data.split('_')[1]
    if size == 'back':
        await callback.message.answer(texts['heart_props_message'], reply_markup=heart_props_keyboard())
        await state.set_state(HeartState.props)
        return
    
    await state.update_data(size=size)

    data = await state.get_data()
    user = users[callback.from_user.id]

    user.heart_style = HeartStyle(
        style_ = data['style'],
        form_ = data['form'],
        color_ = data['color'],
        props_ = data['props'],
        size_ = data['size']
    )

    users[callback.from_user.id] = user

    db_handler.update_user(user)

    await callback.message.answer(texts['show_settings_message'].format(
        username = callback.from_user.username,
        heart_style = user.heart_style.style_,
        heart_form = user.heart_style.form_,
        heart_color = user.heart_style.color_,
        heart_props = user.heart_style.props_,
        heart_size = user.heart_style.size_,
    ))

    await state.clear()

    await callback.answer()



async def main():
    bot = Bot(token=config['token'])
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    logger.info('started polling...')
    