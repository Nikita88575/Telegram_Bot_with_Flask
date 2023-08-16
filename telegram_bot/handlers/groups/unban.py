from aiogram import types
from loader import dp, bot 
from aiogram.types import Message
from filters import IsAdmin, IsGroup
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest
from utils.db_api import quick_commands as sql_commands

@dp.message_handler(IsGroup(), IsAdmin(), commands=['unban'])
@dp.message_handler(IsGroup(), IsAdmin(), Command('unban', prefixes='!'))
async def гтban(message: Message):
    await sql_commands.check_chat_user(message)
    await sql_commands.update_info(message.from_user.id, message.from_user.first_name,
                                   message.from_user.last_name, message.from_user.username)
    if message.reply_to_message:

        if message.reply_to_message.from_user.id == message.from_user.id:
            await message.reply(f'❌ Не можна розблокувати самого себе ❗️')

        else:
            chat_member = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            member_id = message.reply_to_message.from_user.id
            chat_id = message.chat.id
            
            try:
                if chat_member.status == types.ChatMemberStatus.BANNED:
                    await message.reply(f'❗️ Адміністратор {message.from_user.get_mention(as_html=True)} '
                                        f'розблокував(ла) користувача '
                                        f'{message.reply_to_message.from_user.get_mention(as_html=True)}❗️')
                    await bot.unban_chat_member(chat_id, member_id, True)
                elif chat_member.status != types.ChatMemberStatus.BANNED:
                    await message.reply('Цей користувач не заблокован ❗️')
            except BadRequest:
                await message.reply(f'❌ Цього користувача не можна розблокувати ❗️')
    else:
        await message.reply(f'❌ Ця команда працює тільки у відповідь на повідомлення ❗️')