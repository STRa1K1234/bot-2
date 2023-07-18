import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config import token, statuses, var


logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()
data = []


@dp.message(lambda message: message.from_user.id not in statuses and message.content_type == 'text')
async def cmd_start(message: types.Message):
    statuses[message.from_user.id] = {}
    await message.answer(f"<b>Добрый день, коллеги! ✨</b>\n Этот бот создан для нашего с вами удобства в процессе закупа канцелярии!", parse_mode="HTML")
    kb = [
        [types.KeyboardButton(text="Хоз. товары")],
        [types.KeyboardButton(text="Канцелярия")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(f'Выберите тип закупок:', reply_markup=keyboard)



@dp.message(lambda message: (message.from_user.id in statuses
                                           and len(statuses[message.from_user.id]) == 0 and message.text in var))
async def who(message: types.Message):
    statuses[message.from_user.id] = [message.text]
    await message.answer("Введите свое имя и фамилию:")


@dp.message(lambda message: (message.from_user.id in statuses
                                           and len(statuses[message.from_user.id]) == 1))
async def link(message: types.Message):
    statuses[message.from_user.id].append(message.text)
    await message.answer("Прикрепите ссылки и количество:")



@dp.message(lambda message: (message.from_user.id in statuses
                                           and len(statuses[message.from_user.id]) == 2))
async def right(message: types.Message):
    statuses[message.from_user.id].append(message.text)
    kb = [
        [types.KeyboardButton(text="Верно")],
        [types.KeyboardButton(text="Ошибка")]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer('Проверьте правильность написания:\n'
                         f'{statuses[message.from_user.id][1]}\n'
                         f'{statuses[message.from_user.id][2]}\n', reply_markup=keyboard)


@dp.message(lambda message: (message.from_user.id in statuses
                                           and len(statuses[message.from_user.id]) == 3))
async def final(message: types.Message):
    if message.text == 'Верно':
        await bot.send_message(chat_id=-949617998, text=
                             f'{statuses[message.from_user.id][0]}\n'
                             f'{statuses[message.from_user.id][1]}\n'
                             f'{statuses[message.from_user.id][2]}\n')
        del statuses[message.from_user.id]
    else:
        await message.answer("Введите данные заново")
        await message.answer("Введите свое имя и фамилию:")
        del statuses[message.from_user.id][1:]


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())