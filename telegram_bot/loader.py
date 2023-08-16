from aiogram import Bot, Dispatcher, types
from data import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.db_gino import db

storage = MemoryStorage()

#bot api
bot = Bot(token=config.BOT_API, parse_mode=types.ParseMode.HTML)
#dp
dp = Dispatcher(bot, storage=storage)

__all__ = ['bot', 'storage', 'dp', 'db']