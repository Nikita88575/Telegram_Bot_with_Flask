import re
import datetime
from aiogram import types
from loader import dp, bot 
from aiogram.types import Message
from filters import IsAdmin, IsGroup
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest
from utils.db_api import quick_commands as sql_commands

@dp.message_handler(IsGroup(), IsAdmin(), commands=['mute'])
@dp.message_handler(IsGroup(), IsAdmin(), Command('mute', prefixes='!'))
@dp.message_handler(IsGroup(), IsAdmin(), Command('mute', prefixes='.'))
async def mute(message: Message):

    await sql_commands.check_chat_user(message)
    await sql_commands.update_info(message.from_user.id,
                                   message.from_user.first_name,
                                   message.from_user.last_name,
                                   message.from_user.username)

    try:
        user = await sql_commands.select_user(message.from_user.id)
        if user.status == 'banned':
            await message.reply(f'{message.from_user.first_name} ти у чорному списку')

        elif user.status == 'active':
            if message.reply_to_message:

                if message.reply_to_message.from_user.id == message.from_user.id:
                    await message.reply(f'❌ Не можна обмежити себе у надсиланні повідомлень ❗️')

                else:
                    await sql_commands.check_chat_user(message)
                    chat_member = await bot.get_chat_member(message.chat.id, 
                                                            message.reply_to_message.from_user.id)
                    member_id = message.reply_to_message.from_user.id
                    chat_id = message.chat.id

                    OnlyReadPremissions = types.ChatPermissions(can_add_web_page_previews=False,
                                                                can_change_info=False,
                                                                can_invite_users=False,
                                                                can_pin_messages=False,
                                                                can_send_media_messages=False,
                                                                can_send_messages=False,
                                                                can_send_other_messages=False,
                                                                can_send_polls=False)
                    
                    if message.html_text.startswith('!mute'):
                        command = re.compile(r"(!mute) ?(\d+)? "
                        r"?([№;^`~|:!@/#$%^&?*(+)''_=0-9a-zA-Zа-яА-Яа-щА-ЩЬьЮюЯяЇїІіЄєҐґ ]+)?"
                        ).match(message.html_text)

                    elif message.html_text.startswith('/mute'):
                        command = re.compile(r"(/mute) ?(\d+)? "
                        r"?([№;^`~|:!@/#$%^&?*(+)''_=0-9a-zA-Zа-яА-Яа-щА-ЩЬьЮюЯяЇїІіЄєҐґ ]+)?"
                        ).match(message.html_text)

                    elif message.html_text.startswith('.mute'):
                        command = re.compile(r"(.mute) ?(\d+)? "
                        r"?([№;^`~|:!@/#$%^&?*(+)''_=0-9a-zA-Zа-яА-Яа-щА-ЩЬьЮюЯяЇїІіЄєҐґ ]+)?"
                        ).match(message.html_text)

                    time = command.group(2)
                    comment = command.group(3)

                    if not time:
                        time = 0
                    else:
                        time = int(time)
                    if not comment:
                        comment = 'No reason'
                    else:
                        comment = comment
                    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)

                    if int(time) <= 0:
                        try:

                            if chat_member.status != types.ChatMemberStatus.RESTRICTED:
                                await bot.restrict_chat_member(chat_id, member_id, 
                                                            OnlyReadPremissions, until_date)
                                await message.reply(f'🔇 Адміністратор '
                                                    f'{message.from_user.get_mention(as_html=True)} '
                                                    f'обмежив(ла) користувача '
                                                    f'{message.reply_to_message.from_user.get_mention(as_html=True)} '
                                                    f'у можливості надсилати повідомлення ❗️\nПричина: {comment}')
                                
                            elif chat_member.status == types.ChatMemberStatus.RESTRICTED:
                                await message.reply('Цей користувач вже має обмеження ❗️')

                        except BadRequest:
                            await message.reply(f'❌ Цьому користувачеві не можна обмежити можливість надсилати повідоммлення ❗️')

                    else: 
                        try:

                            if chat_member.status != types.ChatMemberStatus.RESTRICTED:
                                await bot.restrict_chat_member(chat_id, member_id, OnlyReadPremissions, until_date)
                                await message.reply(f'🔇 Адміністратор {message.from_user.get_mention(as_html=True)} '
                                                    f'обмежив(ла) користувача '
                                                    f'{message.reply_to_message.from_user.get_mention(as_html=True)} '
                                                    f'у можливості надсилати повідомлення до {str(until_date).split(".")[0]}'
                                                    f'❗️\nПричина: {comment}')
                            elif chat_member.status == types.ChatMemberStatus.RESTRICTED:
                                await message.reply('Цей користувач вже має обмеження ❗️')
                                
                        except BadRequest:
                            await message.reply(f'❌ Цьому користувачеві не можна обмежити можливість надсилати повідоммлення ❗️')

            else:
                await message.reply(f'❌ Ця команда працює тільки у відповідь на повідомлення ❗️')

    except Exception as _ex:
            print(f'[ERROR] {_ex}')