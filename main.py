import openai
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import executor
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.builtin import CommandHelp

openai.api_key = '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'
bot = Bot(token='6116196699:AAHDPW_he78Aud3K3tRmP1pWTYOl2TZBW94')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class AI(StatesGroup):
    talk = State()


async def on_startup(dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("helps", "Вывести справку")
        ]
    )


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")

    await message.answer("\n".join(text))


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1,
                              inline_keyboard=[[InlineKeyboardButton(text="Начать чат с ИИ", callback_data="start")]])
    await message.answer(
        f"Привет, {message.from_user.full_name}! Этот бот написан для статьи. Он предоставит доступ к ChatGPT.",
        reply_markup=kb)


@dp.callback_query_handler(text='start')
async def chat_start(call: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text="Закончить чат", callback_data="start"),
         InlineKeyboardButton(text="Стереть память", callback_data="start")]])

    await call.message.answer("Отправть сообщение, чтобы начать переписку", reply_markup=kb)
    await AI.talk.set()
    await state.update_data(history=[{"question": None, "answer": None}])


@dp.message_handler(state=AI.talk)
async def chat_talk(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data = data.get('history')
    kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text="Закончить чат", callback_data="back"),
         InlineKeyboardButton(text="Стереть память", callback_data="clear")]])
    await message.answer("ИИ думает...", reply_markup=kb)

    history = []
    if len(data) > 1:
        for index in range(0, len(data)):
            if data[index].get('question') is None:
                data[index]['question'] = message.text
                d = {"role": "user", "content": data[index]['question']}
                history.append(d)
            else:
                d = [{"role": "user", "content": data[index]['question']},
                     {"role": "assistant", "content": data[index].get('answer')}]
                history += d
    else:
        data[0]['question'] = message.text
        d = {"role": "user", "content": data[0].get('question')}
        history.append(d)
    print(history)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history,
        max_tokens=500,
        temperature=1,
    )
    resp_ai = request['choices'][0]['message']['content']
    data[-1]['answer'] = resp_ai.replace('\n', '')
    text = f"{message.from_user.username}\nQ:{data[-1]['question']}\nA:{data[-1]['answer']}"
    data.append({"question": None, "answer": None})
    if len(data) > 10:
        await state.update_data(history=[{"question": None, "answer": None}])
    await state.update_data(history=data)
    await message.answer(resp_ai)


@dp.callback_query_handler(text='back', state='*')
async def back(call: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardMarkup(row_width=1,
                              inline_keyboard=[[InlineKeyboardButton(text="Начать чат с ИИ", callback_data="start")]])
    await call.message.answer(
        f"Привет, {call.from_user.full_name}! Этот бот написан для статьи. Он предоставит доступ к ChatGPT.",
        reply_markup=kb)
    await state.finish()


@dp.callback_query_handler(text='clear', state='*')
async def clear(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Память ИИ стерта')
    await state.update_data(history=[{"question": None, "answer": None}])


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
