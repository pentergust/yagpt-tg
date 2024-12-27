"""Клавиатуры бота."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Клавиатура для регистрации нового пользователя
GREETING = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="🍰 принимаю", callback_data="reg")
]])
