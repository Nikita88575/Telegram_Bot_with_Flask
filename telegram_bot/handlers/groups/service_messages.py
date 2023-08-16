from loader import dp
from aiogram import types
from utils.db_api import quick_commands as sql_commands

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome(message: types.Message):
    await sql_commands.check_chat_user(message)
    members = ", ".join([mess.get_mention(as_html=True) for mess in message.new_chat_members])   
    await message.reply(f'{members} приєднався до нас ❗️')

@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def left_or_ban(message: types.Message):
    if message.left_chat_member.id == message.from_user.id:
        await  message.reply(f'{message.from_user.first_name} покинув нас ❗️')
    else:
        await message.reply(f'{message.from_user.get_mention(as_html=True)} вигнав(ла) '
        f'{message.left_chat_member.get_mention(as_html=True)} ❗️')