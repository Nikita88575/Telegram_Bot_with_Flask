from loader import dp
from aiogram import types
from utils.db_api import quick_commands as sql_commands

@dp.message_handler()
@dp.message_handler(content_types=types.ContentTypes.all())
async def messages(message: types.Message):
    await sql_commands.update_info(message.from_user.id,
                                   message.from_user.first_name,
                                   message.from_user.last_name,
                                   message.from_user.username)