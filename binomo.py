from aiogram import types
from aiogram.utils import executor

from admin import send_form, send_graph, send_add_users, send_clear, send_requisit, send_start
from guest import send_authorization, send_support
from bot import bot, dp, admin_id, main_user_bot

user_wait_link = None

@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
	user_id = message.from_user.id

	if user_id in admin_id:
		await send_start(message)
	else:
		await send_authorization(message)

@dp.message_handler(commands = ['link'])
async def get_link(message: types.Message):
	user_id = message.from_user.id

	if user_id == main_user_bot:
		await bot.send_message(user_wait_link, message.text[6:])
	else:
		await answer_text(message)

@dp.message_handler(content_types = ["text"])
async def answer_text(message: types.Message):
	user_id = message.from_user.id

	if user_id in admin_id:
		match message.text:
			case "Вериф":
				await send_form(message)
			case "Доход":
				await send_graph(message)
			case "Cоздать группу":
				await send_create_group(message)
			case "Добавить участника":
				await send_add_users(message)
			case "Очистить":
				await send_clear(message)
			case "Реквезиты":
				await send_requisit(message)
			case _:
				await send_start(message)
	else:
		match message.text:
			case "Поддержка":
				await send_support(message)
			case _:
				await send_authorization(message)

async def send_create_group(message):
	global user_wait_link

	user_wait_link = message.from_user.id
	await bot.send_message(main_user_bot, 'create supergroup')

while True:
	try:
		executor.start_polling(dp)
	except BaseException as ex:
		print(type(ex).__name__ + ":", ex)
