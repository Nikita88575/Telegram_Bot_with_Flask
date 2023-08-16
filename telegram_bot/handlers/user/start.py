from loader import dp
from aiogram import types
from filters.private_chat import IsPrivate
from utils.misc.throttling import rate_limit
from utils.db_api import quick_commands as sql_commands

@rate_limit(limit=2)
@dp.message_handler(IsPrivate(), commands=['start'])
async def start(message: types.Message):
    try:
        user = await sql_commands.select_user(message.from_user.id)
        if user.status == 'banned':
            await message.reply(f'{message.from_user.first_name} ти у чорному списку')
        elif user.status == 'active':
            await sql_commands.update_info(message.from_user.id,
                                           message.from_user.first_name,
                                           message.from_user.last_name,
                                           message.from_user.username)
        
    except Exception:
        if not message.from_user.is_bot:
            await sql_commands.add_user(message.from_user.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)
            try:
                await sql_commands.update_info(message.from_user.id,
                                       message.from_user.first_name,
                                       message.from_user.last_name,
                                       message.from_user.username)
            except Exception as _err:
                print(f'[ERROR] {_err}')
            await message.reply('Ти успішно зареєструвався(acь)')