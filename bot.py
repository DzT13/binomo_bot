import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import assert_test_bot, creator_id, admin_id, main_user_bot

logging.basicConfig(level = logging.INFO)
bot = Bot(token = assert_test_bot, parse_mode = 'html')
dp = Dispatcher(bot, storage = MemoryStorage())

creator_id = creator_id
admin_id = admin_id
main_user_bot = main_user_bot

