from loader import dp 
from aiogram.types import Message
from utils.misc.throttling import rate_limit
from utils.db_api import quick_commands as sql_commands

@rate_limit(limit=1)
@dp.message_handler(commands=['info'])
async def info(message: Message):
    await sql_commands.check_chat_user(message)
    await sql_commands.update_info(message.from_user.id,
                                   message.from_user.first_name,
                                   message.from_user.last_name,
                                   message.from_user.username)

    if message.reply_to_message is None:
        try:
            user = await sql_commands.select_user(message.from_user.id)
            await message.reply(f"👤 Ім'я: {message.from_user.get_mention(as_html=True)}\n"
                                f'👤 Статус: {user.status}\n'
                                f'🗓 У боті з {str(user.created_at).split(".")[0]}\n'
                                f'\n<code>{user.user_id}</code>')
        except Exception as _ex:
            print(f'[ERROR] {_ex}')

    elif message.reply_to_message:
        try:
            user = await sql_commands.select_user(message.from_user.id)
            if user.status == 'banned':
                await message.reply(f'{message.from_user.first_name} ти у чорному списку')

            elif user.status == 'active':
                await sql_commands.check_chat_user(message)
                await sql_commands.update_info(message.from_user.id,
                                               message.from_user.first_name,
                                               message.from_user.last_name,
                                               message.from_user.username)
                try:
                    user = await sql_commands.select_user(message.reply_to_message.from_user.id)
                    await message.reply(f"👤 Ім'я: "
                                        f'{message.reply_to_message.from_user.get_mention(as_html=True)}'
                                        f'\n👤 Статус: {user.status}\n'
                                        f'🗓 У боті з {str(user.created_at).split(".")[0]}\n'
                                        f'\n<code>{user.user_id}</code>')
                except Exception as _ex:
                    print(f'[ERROR] {_ex}')
        except Exception as _ex:
                print(f'[ERROR] {_ex}')