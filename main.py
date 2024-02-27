import requests
import logging

from aiogram import Bot, Dispatcher, types, executor
from states import HolidaysForTheYearState, DateState
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import menu_keyboard, country_keyboard, year_eror

API_TOKEN = '7157606774:AAGa83bmKEtwEBgBaFeSkArL60YwnoIz2m4'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

api_key = 'tdmF62S0QgG80BPJmbvglUtVSErov19c'

@dp.message_handler(commands='start')
async def start(message: types.Message):
      await message.answer(text='Welcome to calendar bot', reply_markup=menu_keyboard)

@dp.message_handler(commands='help')
async def help(message: types.Message):
      await message.reply(text='Доступные команды:')

@dp.message_handler(text='🌏 Holidays for the year')
async def HolidaysForTheYear(message: types.Message):
      await message.answer(text='Enter the name of the country', reply_markup=country_keyboard)
      await HolidaysForTheYearState.country.set()
      await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@dp.callback_query_handler(state=HolidaysForTheYearState.country)
async def HolidaysForTheYearCountry(call: types.CallbackQuery, state: FSMContext):
      country = call.data
      await state.update_data(
            {
                  'country': country
            }
      )
      await call.message.answer(text='Enter the year')
      await HolidaysForTheYearState.year.set()
      await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@dp.message_handler(state=HolidaysForTheYearState.year)
async def HolidaysForTheYearYear(message: types.Message, state: FSMContext):
      year = message.text
      await state.update_data(
            {
                  'year': year
            }
      )
      data = await state.get_data()
      year = data['year']
      country = data['country']
      url = requests.get(f"https://calendarific.com/api/v2/holidays?&api_key=tdmF62S0QgG80BPJmbvglUtVSErov19c&country={country}&year={year}")
      data = url.json()
      result = ''
      counter = 1
      if len(data['response']) != 0:
            for i in data['response']['holidays'][:20]:
                  result += f'#{counter}\nName: {i["name"]}\nDescription: {i["description"]}\nDate: {i["date"]["datetime"]["month"]}.{i["date"]["datetime"]["day"]}.{i["date"]["datetime"]["year"]}\n\n'
                  counter += 1
            await message.reply(text=result)
            await state.finish()
      else:
            await message.reply(text='The date you entered is not supported', reply_markup=year_eror)
            await HolidaysForTheYearState.year_error.set()

@dp.callback_query_handler(state=HolidaysForTheYearState.year_error, text='close')
async def close(call: types.CallbackQuery, state: FSMContext):
      await state.finish()
      await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@dp.callback_query_handler(state=HolidaysForTheYearState.year_error, text='retry')
async def retry(call: types.CallbackQuery, state: FSMContext):
      await call.message.answer(text='Enter year')
      await HolidaysForTheYearState.year.set()
      await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@dp.message_handler(text='📆 Weekend check')
async def WeekendCheck(message: types.Message):
      await message.answer(text='Enter date\n YYYY-MM-DD')
      await DateState.date.set()

@dp.message_handler(state=DateState.date)
async def WeekendCheckDate(message: types.Message, state: FSMContext):
      date = message.text
      url = requests.get(f"https://isdayoff.ru/{date}?covid=[0|1]?pre=[0|1]")
      data = url.json()
      if data == 1:
            await message.reply(text='Day off 😊')
      elif data == 2:
            await message.reply(text='Part-time 😏')
      elif data == 0:
            await message.reply(text='Working day 😒')
      else:
            await message.reply(text='Date entered incorrectly\nYYYY-MM-DD')
      await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
