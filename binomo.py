from aiogram import types
from aiogram.utils import executor

from user import User
from bot import bot, dp

@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
	user = User(message)

	if user.status is User.status.Admin:
		await user.send_start()
	else:
		await user.send_authorization()

@dp.message_handler(commands = ['link'])
async def get_link(message: types.Message):
	user = User(message)

	if user.status is User.status.MainUserBot:
		await bot.send_message(user.user_wait_link, message.text[6:])
	else:
		await answer_text(message)

@dp.message_handler(content_types = ["text"])
async def answer_text(message: types.Message):
	user = User(message)

	if user.status is User.status.Admin:
		match message.text:
			case "Вериф":
				await user.send_form()
			case "Доход":
				await user.send_graph()
			case "Cоздать группу":
				await user.send_create_group()
			case "Добавить участника":
				await user.send_add_users()
			case "Очистить":
				await user.send_clear()
			case "Реквезиты":
				await user.send_requisit()
			case _:
				await user.send_start()
	else:
		match message.text:
			case "Поддержка":
				await user.send_support()
			case _:
				await user.send_authorization()

while True:
	try:
		executor.start_polling(dp)
	except BaseException as ex:
		print(type(ex).__name__ + ":", ex)
