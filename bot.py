import sys

sys.path.append('D:/sublime/bot/bot_api')
sys.path.append('D:/sublime/orders/user_id')

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_api import assert_test_bot
from binomo_id import admin_id, main_user_bot

bot = Bot(token = assert_test_bot, parse_mode = 'html')
dp = Dispatcher(bot, storage = MemoryStorage())

admin_id = admin_id
main_user_bot = main_user_bot