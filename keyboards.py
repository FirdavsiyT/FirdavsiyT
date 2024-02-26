from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Default keyboards

menu_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton('🌏 Holidays for the year'),
            KeyboardButton('📆 Weekend check')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Inline keyboards

country_keyboard = InlineKeyboardMarkup(row_width=1)
ru = InlineKeyboardButton('🇷🇺 Russia', callback_data='RU')
uz = InlineKeyboardButton('🇺🇿 Uzbekistan', callback_data='UZ')
us = InlineKeyboardButton('🇱🇷 USA', callback_data='US')
uk = InlineKeyboardButton('🇬🇧 UK', callback_data='UK')
country_keyboard.add(ru, uz, us, uk)

year_eror = InlineKeyboardMarkup(row_width=2)
close = InlineKeyboardButton('❌ Close', callback_data='close')
retry = InlineKeyboardButton('📝 Write another code', callback_data='retry')
year_eror.add(close, retry)