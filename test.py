# @dp.message_handler(commands=['start'])
# async def StartCommands(message: types.Message):
#     await message.reply('Добрый день, я нейросеть chat-gtp чечня лев чемпион.')
#
#
# @dp.message_handler()
# async def respond_to_message(message: types.Message):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=str(message.text),
#         temperature=1,
#         max_tokens=1024,
#         top_p=0.7,
#         frequency_penalty=0,
#     )
#     await message.reply(response.choices[0].text.strip())