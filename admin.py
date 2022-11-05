from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os
import re
from json import load, dump
from random import randrange

from change_image import change_graph, change_form
from bot import bot, dp


class Form(StatesGroup):
	add_users = State()
	form = State()
	graph = State()
	requisit = State()


async def send_start(message):
	await bot.send_message(message.chat.id, "Выберите Вериф или Доход", reply_markup = button_admin())

async def send_add_users(message):
	await bot.send_message(message.chat.id, text_add_users, reply_markup = button_admin())
	await Form.add_users.set()

async def send_form(message):
	await bot.send_message(message.chat.id, text_form, reply_markup = button_admin())
	await Form.form.set()

async def send_graph(message):
	await bot.send_message(message.chat.id, text_graph, reply_markup = button_admin())
	await Form.graph.set()

async def send_requisit(message):
	await bot.send_message(message.chat.id, "Введите реквизиты для инвестиций:", reply_markup = button_admin())
	await Form.requisit.set()

async def send_clear(message):
	with open("users.json", "w") as f:
		dump(dict(), f, indent = 4, ensure_ascii = False)

	await bot.send_message(message.chat.id, "База данных успешно очищенна", reply_markup = button_admin())

@dp.message_handler(state = Form.add_users)
async def handle_add_users(message: types.Message, state: FSMContext):
	await state.finish()

	args = message.text.split('\n')
	if len(args) != 5:
		return await bot.send_message(message.chat.id, "Ввод не верный", reply_markup = button_admin())

	if not(os.path.exists("requisits.json")):
		return await bot.send_message(message.chat.id, "Вы ещё не ввели реквизиты", reply_markup = button_admin())

	full_name, deposit, data, broker, active_trading = args
	if broker not in {'1', '2'}:
		return await bot.send_message(message.chat.id, text_broker_not_correct, reply_markup = button_admin())

	db = dict()
	if os.path.exists("users.json"):
		with open("users.json", "r", encoding = "utf8") as f:
			db = load(f)

	if len(db.keys()) >= 89999:
		return await bot.send_message(message.chat.id, "База данных переполнена", reply_markup = button_admin())

	slot = randrange(10000, 99999)
	while slot in db.keys():
		slot = randrange(10000, 99999)

	db[slot] = {
		"ФИО" : full_name,
		"депозит" : deposit,
		"дата": data,
		"брокер": broker,
		"aктив торговли": active_trading
	}

	with open("users.json", "w", encoding = "utf8") as f:
		dump(db, f, indent = 4, ensure_ascii = False)

	with open("requisits.json", "r", encoding = "utf8") as f:
		requisit = load(f)

	text = text_slot_created.format(slot, full_name, deposit, requisit)
	await bot.send_message(message.chat.id, text, reply_markup = button_admin())

@dp.message_handler(state = Form.form)
async def handle_form(message: types.Message, state: FSMContext):
	await state.finish()

	args = message.text.split('\n')
	if len(args) != 4:
		return await bot.send_message(message.chat.id, "Ввод не верный", reply_markup = button_admin())

	full_name, deposit, data, income = args
	if len(full_name) > 14:
		full_name = full_name[:13] + ".."

	await change_form(message, full_name, deposit, data, income)

@dp.message_handler(state = Form.graph)
async def handle_graph(message: types.Message, state: FSMContext):
	await state.finish()

	args = message.text.split('\n')
	if len(args) != 7:
		return await bot.send_message(message.chat.id, "Ввод не верный", reply_markup = button_admin())

	full_name, deposit, data, income, broker, active_trading, total_income = message.text.split('\n')

	if broker not in {'1', '2'}:
		return await bot.send_message(message.chat.id, text_broker_not_correct, reply_markup = button_admin())

	if len(full_name) > 14:
		full_name = full_name[:13] + ".."

	total_income = float(total_income)
	broker_income = total_income * (400 / 1041)
	client_income = total_income * (206 / 347)

	await change_graph(message, full_name, deposit, data, income, broker, active_trading, total_income, broker_income, client_income)

@dp.message_handler(state = Form.requisit)
async def handle_requisit(message: types.Message, state: FSMContext):
	await state.finish()

	text = message.text
	sample = re.search(r"^\d{4}([_\- ]*\d{4}){3}$", text)

	if sample is None:
		return await bot.send_message(message.chat.id, "Реквизиты введенны не верно", reply_markup = button_admin())

	with open("requisits.json", "w", encoding = "utf8") as f:
		dump(text, f, indent = 4, ensure_ascii = False)

	await bot.send_message(message.chat.id, "Реквизиты успешно добавлены", reply_markup = button_admin())

def button_admin():
	markup = ReplyKeyboardMarkup(resize_keyboard = True)
	markup.add(KeyboardButton("Вериф"), KeyboardButton("Доход"), KeyboardButton("Cоздать группу"))
	markup.add(KeyboardButton("Добавить участника"), KeyboardButton("Очистить"), KeyboardButton("Реквезиты"))

	return markup

text_add_users = """
ФИО:
Депозит:
Дата:
Брокер:
Актив торговли:
"""

text_slot_created = """
🧾<b>Слот</b> №<code>{}</code> создан
👤<b>Инвестор</b>: {}
💵<b>Депозит</b>: {} руб
💳<b>Реквизиты для инвестиций</b>: <code>{}</code>

<i>Реквизиты действительны 15 минут</i>
"""

text_form = """
ФИО:
Депозит:
Дата:
Доход:
"""

text_graph = """
ФИО:
Депозит:
Дата:
Доход:
Брокер:
Актив торговли:
Общий доход:
"""

text_broker_not_correct = """
Брокер введён не верно, введите номер брокера:
1: Romanenko Invest Capital
2: Фонд помощи
"""