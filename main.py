import openai
from aiogram import executor, Bot, Dispatcher, types

openai.api_key = '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'
bot = Bot(token='6116196699:AAHDPW_he78Aud3K3tRmP1pWTYOl2TZBW94')
dp = Dispatcher(bot)


async def responseget():
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=str(message.text),
        temperature=1,
        max_tokens=1024,
        top_p=0.7,
        frequency_penalty=0,
    )
    return response.choices[0].text.strip()


@dp.message_handler()
async def respond_to_message(message: types.Message):
    await message.reply(await responseget())


if __name__ == '__main__':
    executor.start_polling(dp)
