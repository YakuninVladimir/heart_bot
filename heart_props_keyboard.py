from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class HeartState(StatesGroup):
    style = State()
    form = State()
    color = State()
    props = State()
    size = State()

def heart_style_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="абстрактное", callback_data="style_abstract")],
        [InlineKeyboardButton(text="облачное", callback_data="style_cloudy")],
        [InlineKeyboardButton(text="кристаллическое", callback_data="style_crystal")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="style_back")]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard,
    )

def heart_form_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="округлый", callback_data="form_round")],
        [InlineKeyboardButton(text="остроконечный", callback_data="form_sharp")],
        [InlineKeyboardButton(text="свой вариант (качество может отличаться)", callback_data="form_custom")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="form_back")]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard,
    )

def heart_color_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="красный", callback_data="color_red")],
        [InlineKeyboardButton(text="розовый", callback_data="color_pink")],
        [InlineKeyboardButton(text="синий", callback_data="color_blue")],
        [InlineKeyboardButton(text="зеленый", callback_data="color_green")],
        [InlineKeyboardButton(text="желтый", callback_data="color_yellow")],
        [InlineKeyboardButton(text="черный", callback_data="color_black")],
        [InlineKeyboardButton(text="белый", callback_data="color_white")],
        [InlineKeyboardButton(text="свой цвет", callback_data="color_custom")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="color_back")]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard,
    )

def heart_props_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="огонь", callback_data="props_fire")],
        [InlineKeyboardButton(text="вода", callback_data="props_water")],
        [InlineKeyboardButton(text="дым", callback_data="props_smoke")],
        [InlineKeyboardButton(text="пламя", callback_data="props_flame")],
        [InlineKeyboardButton(text="свет", callback_data="props_light")],
        [InlineKeyboardButton(text="тени", callback_data="props_shadows")],
        [InlineKeyboardButton(text="блики", callback_data="props_glare")],
        [InlineKeyboardButton(text="свой эффект", callback_data="props_custom")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="props_back")]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard,
    )

def heart_size_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="маленький", callback_data="size_small")],
        [InlineKeyboardButton(text="средний", callback_data="size_medium")],
        [InlineKeyboardButton(text="большой", callback_data="size_large")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="size_back")]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard,
    )
