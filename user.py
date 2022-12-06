from admin import Admin, MainUserBot
from guest import Guest
from bot import admin_id, main_user_bot

class Status:
	Admin = Admin
	Guest = Guest
	MainUserBot = MainUserBot

def User(message):
	User.status = Status
	user_id = message.from_user.id

	if user_id in admin_id:
		return Admin(message)

	if user_id == main_user_bot:
		return MainUserBot(message)

	return Guest(message)