import asyncio
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os
from json import load, dump
from random import shuffle
from numpy import arange
from datetime import datetime
from dataclasses import dataclass

from change_image import change_graph
from bot import bot, dp


class Form(StatesGroup):
	authorization = State()


@dataclass
class Guest:
	def __init__(self, message):
		self.status = type(self)
		self.message = message

	async def send_authorization(self):
		await bot.send_message(self.message.chat.id, text_authorization, reply_markup = button_users())
		await Form.authorization.set()

	async def send_support(self):
		await bot.send_message(self.message.chat.id, text_support, reply_markup = button_users())


@dp.message_handler(state = Form.authorization)
async def handle_authorization(message: types.Message, state: FSMContext):
	await state.finish()

	if not(os.path.exists("users.json")):
		return await bot.send_message(message.chat.id, text_not_correct_slot, reply_markup = button_users())

	slot = message.text
	with open("users.json", "r", encoding = "utf8") as f:
		db = load(f)
		user = db.get(slot)

	if user is None:
		return await bot.send_message(message.chat.id, text_not_correct_slot, reply_markup = button_users())

	db.pop(slot)
	with open("users.json", "w", encoding = "utf8") as f:
		dump(db, f, indent = 4, ensure_ascii = False)

	full_name = user["ФИО"]
	deposit = user["депозит"]
	data = user["дата"]
	broker = user["брокер"]
	active_trading = user["aктив торговли"]

	overall_balance = float(deposit) + 300
	overall_balance = {int(overall_balance): int(overall_balance)}.get(overall_balance, overall_balance)
	total_income = 104000 if overall_balance <= 2500 else (180000 if 2501 <= overall_balance <= 5000 else 270000)

	text = text_start_trading.format(full_name, deposit, overall_balance)
	await bot.send_message(message.chat.id, text, reply_markup = button_users())

	hour_before = 33 if datetime.now().hour > 0 else 9
	time_must_letter = hour_before - datetime.now().hour
	wait_minute = (60 - datetime.now().minute) * 60
	list_money = get_list_money(time_must_letter, overall_balance, total_income)
	total = overall_balance

	await send_salary(message, time_must_letter, list_money, total)
	await asyncio.sleep(wait_minute)

	total_income = {int(total_income): int(total_income)}.get(total_income, total_income)
	broker_income = total_income * (400 / 1041)
	client_income = total_income * (206 / 347)

	text = text_end_trading.format(total_income, client_income)
	if len(full_name) > 14:
		full_name = full_name[:13] + ".."

	await bot.send_message(message.chat.id, text, reply_markup = button_users())
	await change_graph(message, full_name, deposit, data, total_income, broker, active_trading, total_income, broker_income, client_income, slot)
	await bot.send_message(message.chat.id, text_contact_broker, reply_markup = button_users())

async def send_salary(message, time_must_letter, list_money, total, i = 0):
	if i < time_must_letter - 3:
		await asyncio.sleep(3600)

		earn = list_money[i]
		total = round(total + earn, 3)
		text = text_trading.format(earn, total)
		await bot.send_message(message.chat.id, text, reply_markup = button_users())

		await send_salary(message, time_must_letter, list_money, total, i + 1)

def get_list_money(time_must_letter, overall_balance, total_income):
	profit = total_income - overall_balance - ((total_income - overall_balance) / time_must_letter * (60 - datetime.now().minute)) / 60
	money_interval = profit / (time_must_letter - 1)

	step = 2 / (time_must_letter - 2)
	arr_coef = [round(i, 3) for i in arange(1, 3 + step, step)]
	shuffle(arr_coef)
	list_money = [round((money_interval / 2) * j, 3)  for i, j in zip(range(time_must_letter - 1), arr_coef)]

	return list_money

def button_users():
	markup = ReplyKeyboardMarkup(resize_keyboard = True)
	markup.add(KeyboardButton("Вход"), KeyboardButton("Поддержка"))

	return markup

text_start_trading = """
👋{}, здравствуйте
💳<b>Сумма вашего депозита</b>: {}₽
📈<i>Торговля уже началась</i>📈
⏰<i>Время выплаты 09:00</i>
<b>Заработано:</b> 300₽
<b>Общий баланс:</b> {}₽
"""

text_trading = """
💵<b>Вы зарботали:</b> {}₽
👉<b>Общий баланс:</b> {}₽
"""

text_end_trading = """
✔<b>Торговля окончена</b>✔
----------------------------------------
💳 Ваш заработок: {}₽
💼 Доля брокера 40%
💵 Ваш доход: {:.3f}₽
"""

text_authorization = "👉 Для авторизации отправите номер <b>слота</b> который выдал вам брокер"
text_not_correct_slot = "❌<b>Вы ввели неверный номер слота</b>❌"
text_contact_broker = "👉 Cвяжитесь с вашим брокером и отправьте реквизиты для получения выплаты 💵"
text_support = 'Вы можете связаться со <b>службой поддержки</b> через: <b><a href="https://t.me/binomo_russia">binomo_russia</a></b>'